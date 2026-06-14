import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api";

export default function ReviewClaim() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    claim: id,
    reviewer: 1,
    decision: "APPROVE",
    approved_amount: "",
    comment: "",
  });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await API.post("/reviews/human-reviews/", form);
    navigate(`/claims/${id}`);
  };

  return (
    <div>
      <h2>Human Review</h2>
      <form onSubmit={handleSubmit}>
        <select name="decision" onChange={handleChange}>
          <option value="APPROVE">Approve</option>
          <option value="REJECT">Reject</option>
          <option value="REQUEST_MORE_DOCUMENTS">Request More Documents</option>
          <option value="PARTIALLY_APPROVE">Partially Approve</option>
        </select>
        <br /><br />

        <input name="approved_amount" placeholder="Approved Amount" onChange={handleChange} />
        <br /><br />

        <textarea name="comment" placeholder="Review Comment" onChange={handleChange}></textarea>
        <br /><br />

        <button>Submit Review</button>
      </form>
    </div>
  );
}