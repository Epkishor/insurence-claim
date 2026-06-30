import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import API from "../api";
import { aiProcessClaim } from "../api/claimsApi";

export default function ClaimDetails() {
  const { id } = useParams();
  const [claim, setClaim] = useState(null);
  const [aiResult, setAiResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  const loadClaim = () => {
    API.get(`/claims/claims/${id}/`).then((res) => setClaim(res.data));
  };

  useEffect(() => {
    loadClaim();
  }, [id]);

  const processClaim = async () => {
    await API.post(`/claims/claims/${id}/process/`);
    loadClaim();
  };

  const runAiProcessing = async () => {
    try {
      setAiLoading(true);
      setAiError("");

      const result = await aiProcessClaim(id);
      setAiResult(result.ai_result);
      setClaim(result.claim);
    } catch (error) {
      setAiError("AI processing failed. Please check backend server and uploaded claim data.");
    } finally {
      setAiLoading(false);
    }
  };

  if (!claim) return <p>Loading...</p>;

  const finalDecision = aiResult?.final_decision;
  const fraudAnalysis = aiResult?.risk_fraud_analysis;

  return (
    <div className="claim-details-page">
      <div className="claim-details-header">
        <div>
          <p className="dashboard-kicker">Claim #{claim.id}</p>
          <h2>Claim Details</h2>
          <p>Review claim data and run AI-assisted claim processing.</p>
        </div>

        <div className="claim-actions">
          <button onClick={runAiProcessing} disabled={aiLoading} className="ai-action-button">
            {aiLoading ? "Running AI..." : "Run AI Processing"}
          </button>
          <button onClick={processClaim} className="secondary-action-button">
            Basic Process
          </button>
        </div>
      </div>

      {aiError && <div className="auth-error">{aiError}</div>}

      <div className="claim-details-grid">
        <section className="dashboard-panel claim-info-panel">
          <div className="dashboard-panel-header">
            <div>
              <h2>Claim Information</h2>
              <p>Patient, hospital, policy, and claim amount.</p>
            </div>
          </div>

          <div className="claim-info-list">
            <InfoRow label="Patient" value={claim.patient_name} />
            <InfoRow label="Hospital" value={claim.hospital_name} />
            <InfoRow label="Policy" value={claim.policy_number} />
            <InfoRow label="Diagnosis" value={claim.diagnosis} />
            <InfoRow label="Treatment" value={claim.treatment_type} />
            <InfoRow label="Claimed Amount" value={formatCurrency(claim.claimed_amount)} />
            <InfoRow label="Approved Amount" value={claim.approved_amount ? formatCurrency(claim.approved_amount) : "Not decided"} />
            <InfoRow label="Status" value={claim.status} />
            <InfoRow label="Decision Reason" value={claim.decision_reason || "No decision yet"} />
          </div>
        </section>

        <section className="dashboard-panel ai-result-panel">
          <div className="dashboard-panel-header">
            <div>
              <h2>AI Processing Result</h2>
              <p>Supervisor Agent output from the backend AI pipeline.</p>
            </div>
          </div>

          {finalDecision ? (
            <div className="ai-result-content">
              <div className="ai-result-metrics">
                <div>
                  <span>Decision</span>
                  <strong>{finalDecision.decision}</strong>
                </div>
                <div>
                  <span>Approved Amount</span>
                  <strong>{formatCurrency(finalDecision.approved_amount)}</strong>
                </div>
                <div>
                  <span>Fraud Risk</span>
                  <strong>{finalDecision.risk_score} / 100</strong>
                </div>
              </div>

              <div className="ai-explanation-box">
                <h3>Explanation</h3>
                <p>{finalDecision.explanation}</p>
              </div>

              <div className="ai-explanation-box">
                <h3>Risk Summary</h3>
                <p>{fraudAnalysis?.risk_summary || "No risk summary available."}</p>
              </div>

              <div className="ai-explanation-box">
                <h3>Human Review</h3>
                <p>{finalDecision.requires_human_review ? "Required" : "Not required"}</p>
              </div>
            </div>
          ) : (
            <div className="dashboard-empty">
              Click “Run AI Processing” to generate the AI claim decision.
            </div>
          )}
        </section>
      </div>

      <div className="claim-footer-links">
        <Link to={`/claims/${id}/upload`}>Upload More Documents</Link>
        <Link to={`/claims/${id}/review`}>Human Review</Link>
        <Link to="/claims">Back to Claims</Link>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="claim-info-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatCurrency(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "N/A";
  return `Rs. ${number.toLocaleString("en-IN")}`;
}
