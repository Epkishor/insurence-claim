import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api";

export default function Dashboard() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    API.get("/claims/claims/")
      .then((res) => setClaims(Array.isArray(res.data) ? res.data : []))
      .catch(() => setClaims([]));
  }, []);

  const approved = claims.filter((c) => normalizeStatus(c.status) === "approved").length;
  const rejected = claims.filter((c) => normalizeStatus(c.status) === "rejected").length;
  const pending = claims.filter((c) => {
    const status = normalizeStatus(c.status);
    return status.includes("pending") || status.includes("review");
  }).length;
  const highRisk = claims.filter((c) => Number(c.fraud_score || c.fraudRiskScore || 0) >= 70).length;

  const metrics = [
    { label: "Total Claims", value: claims.length, note: "All submitted claims", color: "metric-blue" },
    { label: "Approved", value: approved, note: "Ready for settlement", color: "metric-green" },
    { label: "Rejected", value: rejected, note: "Declined after review", color: "metric-red" },
    { label: "Pending Review", value: pending, note: "Needs action or review", color: "metric-amber" },
  ];

  const recentClaims = claims.slice(0, 5);

  return (
    <main className="dashboard-page">
      <section className="dashboard-shell">
        <div className="dashboard-hero">
          <div>
            <p className="dashboard-kicker">Insurance Claim Platform</p>
            <h1>Claim Processing Dashboard</h1>
            <p className="dashboard-hero-text">
              Monitor patient claims, document verification, policy eligibility, fraud risk,
              and final decisions from one professional workspace.
            </p>

            <div className="dashboard-actions">
              <Link className="dashboard-btn dashboard-btn-primary" to="/claims/create">
                Create Claim
              </Link>
              <Link className="dashboard-btn dashboard-btn-secondary" to="/patients/create">
                Add Patient
              </Link>
              <Link className="dashboard-btn dashboard-btn-secondary" to="/claims">
                View Claims
              </Link>
            </div>
          </div>

          <div className="dashboard-health-card">
            <span>System health</span>
            <strong>{highRisk}</strong>
            <p>High-risk claims detected from the current claim records.</p>
          </div>
        </div>

        <div className="dashboard-grid">
          {metrics.map((item) => (
            <article className="metric-card" key={item.label}>
              <span className={`metric-label ${item.color}`}>{item.label}</span>
              <div className="metric-value">{item.value}</div>
              <p className="metric-note">{item.note}</p>
            </article>
          ))}
        </div>

        <div className="dashboard-content-grid">
          <section className="dashboard-panel">
            <div className="dashboard-panel-header">
              <div>
                <h2>Recent Claims</h2>
                <p>Latest claim submissions from hospitals and patients.</p>
              </div>
              <Link to="/claims">View all</Link>
            </div>

            {recentClaims.length > 0 ? (
              <div className="dashboard-table-wrap">
                <table className="dashboard-table">
                  <thead>
                    <tr>
                      <th>Claim ID</th>
                      <th>Patient</th>
                      <th>Amount</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentClaims.map((claim) => (
                      <tr key={claim.id || claim.claim_id}>
                        <td>{claim.claim_number || claim.claim_id || `CLM-${claim.id}`}</td>
                        <td>{getPatientName(claim)}</td>
                        <td>{formatAmount(claim.claim_amount || claim.amount || claim.total_amount)}</td>
                        <td>
                          <StatusBadge status={claim.status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="dashboard-empty">
                No claims found yet. Create your first claim to start the workflow.
              </div>
            )}
          </section>

          <section className="dashboard-panel">
            <div className="dashboard-panel-header">
              <div>
                <h2>AI Claim Workflow</h2>
                <p>Simplified agent process for your project.</p>
              </div>
            </div>

            <div className="workflow-list">
              {[
                ["Document & Medical Analysis", "OCR, reports, bills, and discharge summary checks"],
                ["Policy & Eligibility Check", "Coverage limits, waiting period, and exclusions"],
                ["Risk & Fraud Detection", "Duplicate claims and suspicious billing patterns"],
                ["Claim Decision & Explanation", "Payable amount, policy clauses, and reasoning"],
                ["Human Review", "Final approval for high-risk or uncertain claims"],
              ].map(([title, text], index) => (
                <div className="workflow-step" key={title}>
                  <div className="workflow-step-number">{index + 1}</div>
                  <div>
                    <strong>{title}</strong>
                    <span>{text}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

function StatusBadge({ status }) {
  const normalized = normalizeStatus(status);
  const className = normalized.replaceAll("_", "-").replaceAll(" ", "-");

  return (
    <span className={`status-badge status-${className}`}>
      {formatStatus(status)}
    </span>
  );
}

function normalizeStatus(status = "") {
  return String(status).toLowerCase().replaceAll("_", "-");
}

function formatStatus(status = "Pending") {
  return String(status)
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function getPatientName(claim) {
  if (claim.patient_name) return claim.patient_name;
  if (claim.patient?.full_name) return claim.patient.full_name;
  if (claim.patient?.name) return claim.patient.name;
  if (claim.patient) return `Patient #${claim.patient}`;
  return "Not assigned";
}

function formatAmount(amount) {
  const value = Number(amount);
  if (!Number.isFinite(value)) return "N/A";
  return `Rs. ${value.toLocaleString("en-IN")}`;
}
