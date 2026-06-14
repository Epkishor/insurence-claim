import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import API from "../api";

export default function ClaimDetails() {
  const { id } = useParams();
  const [claim, setClaim] = useState(null);

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

  if (!claim) return <p>Loading...</p>;

  return (
    <div>
      <h2>Claim Details</h2>
      <p>Claim ID: {claim.id}</p>
      <p>Patient: {claim.patient_name}</p>
      <p>Hospital: {claim.hospital_name}</p>
      <p>Policy: {claim.policy_number}</p>
      <p>Diagnosis: {claim.diagnosis}</p>
      <p>Treatment: {claim.treatment_type}</p>
      <p>Claimed Amount: {claim.claimed_amount}</p>
      <p>Approved Amount: {claim.approved_amount || "Not decided"}</p>
      <p>Status: {claim.status}</p>
      <p>Decision Reason: {claim.decision_reason || "No decision yet"}</p>

      <button onClick={processClaim}>Process Claim</button>
      <br /><br />
      <Link to={`/claims/${id}/upload`}>Upload More Documents</Link>
      <br /><br />
      <Link to={`/claims/${id}/review`}>Human Review</Link>
    </div>
  );
}