import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api";

export default function UploadDocuments() {
  const { id } = useParams();
  const [documentType, setDocumentType] = useState("HOSPITAL_BILL");
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append("claim", id);
    data.append("document_type", documentType);
    data.append("file", file);

    await API.post("/documents/claim-documents/", data);
    navigate(`/claims/${id}`);
  };

  return (
    <div>
      <h2>Upload Documents</h2>
      <form onSubmit={handleSubmit}>
        <select onChange={(e) => setDocumentType(e.target.value)}>
          <option value="INSURANCE_CARD">Insurance Card</option>
          <option value="CITIZENSHIP">Citizenship / ID</option>
          <option value="MEDICAL_REPORT">Medical Report</option>
          <option value="PRESCRIPTION">Prescription</option>
          <option value="HOSPITAL_BILL">Hospital Bill</option>
          <option value="DISCHARGE_SUMMARY">Discharge Summary</option>
          <option value="LAB_REPORT">Lab Report</option>
          <option value="OTHER">Other</option>
        </select>
        <br /><br />
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <br /><br />
        <button>Upload</button>
      </form>
    </div>
  );
}