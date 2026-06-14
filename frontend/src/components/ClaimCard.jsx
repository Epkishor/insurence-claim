import { Link } from "react-router-dom";
import StatusBadge from "./StatusBadge";

export default function ClaimCard({ claim }) {
  return (
    <div style={styles.card}>
      <h3>Claim #{claim.id}</h3>

      <p>
        <strong>Patient:</strong> {claim.patient_name || claim.patient}
      </p>

      <p>
        <strong>Hospital:</strong> {claim.hospital_name || claim.hospital}
      </p>

      <p>
        <strong>Policy:</strong> {claim.policy_number || claim.policy}
      </p>

      <p>
        <strong>Claimed Amount:</strong> {claim.claimed_amount}
      </p>

      <p>
        <strong>Status:</strong> <StatusBadge status={claim.status} />
      </p>

      <Link to={`/claims/${claim.id}`}>View Details</Link>
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #ddd",
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
    background: "white",
  },
};