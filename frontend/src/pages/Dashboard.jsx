import { useEffect, useState } from "react";
import API from "../api";

export default function Dashboard() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    API.get("/claims/claims/").then((res) => setClaims(res.data));
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Total Claims: {claims.length}</p>
      <p>Approved: {claims.filter((c) => c.status === "APPROVED").length}</p>
      <p>Rejected: {claims.filter((c) => c.status === "REJECTED").length}</p>
      <p>Pending: {claims.filter((c) => c.status === "PENDING_DOCUMENTS").length}</p>
    </div>
  );
}