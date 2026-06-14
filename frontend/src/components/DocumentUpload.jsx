import { useState } from "react";
import { uploadClaimDocument } from "../api/documentsApi";

export default function DocumentUpload({ claimId, onUploaded }) {
  const [documentType, setDocumentType] = useState("HOSPITAL_BILL");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("claim", claimId);
    formData.append("document_type", documentType);
    formData.append("file", file);

    setLoading(true);

    try {
      await uploadClaimDocument(formData);
      setFile(null);

      if (onUploaded) {
        onUploaded();
      }

      alert("Document uploaded successfully");
    } catch (error) {
      alert("Document upload failed");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleUpload} style={styles.form}>
      <h3>Upload Document</h3>

      <select
        value={documentType}
        onChange={(e) => setDocumentType(e.target.value)}
      >
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

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button disabled={loading}>
        {loading ? "Uploading..." : "Upload Document"}
      </button>
    </form>
  );
}

const styles = {
  form: {
    border: "1px solid #ddd",
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
    background: "#f8fafc",
  },
};