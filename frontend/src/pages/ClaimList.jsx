import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api";

export default function ClaimList() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    API.get("/claims/claims/").then((res) => setClaims(res.data));
  }, []);

  return (
    <div>
      <h2>All Claims</h2>
      {claims.map((claim) => (
        <div key={claim.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
          <h3>Claim #{claim.id}</h3>
          <p>Patient: {claim.patient_name}</p>
          <p>Claimed Amount: {claim.claimed_amount}</p>
          <p>Status: {claim.status}</p>
          <Link to={`/claims/${claim.id}`}>View Details</Link>
        </div>
      ))}
    </div>
  );
}