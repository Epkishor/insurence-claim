import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

export default function CreateClaim() {
  const [form, setForm] = useState({});
  const [patients, setPatients] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [policies, setPolicies] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    API.get("/claims/patients/").then((res) => setPatients(res.data));
    API.get("/users/hospitals/").then((res) => setHospitals(res.data));
    API.get("/policies/policies/").then((res) => setPolicies(res.data));
  }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await API.post("/claims/claims/", form);
    navigate(`/claims/${res.data.id}/upload`);
  };

  return (
    <div>
      <h2>Create Claim</h2>
      <form onSubmit={handleSubmit}>
        <select name="patient" onChange={handleChange}>
          <option>Select Patient</option>
          {patients.map((p) => <option key={p.id} value={p.id}>{p.full_name}</option>)}
        </select><br /><br />

        <select name="hospital" onChange={handleChange}>
          <option>Select Hospital</option>
          {hospitals.map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
        </select><br /><br />

        <select name="policy" onChange={handleChange}>
          <option>Select Policy</option>
          {policies.map((p) => <option key={p.id} value={p.id}>{p.policy_number}</option>)}
        </select><br /><br />

        <input name="diagnosis" placeholder="Diagnosis" onChange={handleChange} /><br /><br />
        <input name="treatment_type" placeholder="Treatment Type" onChange={handleChange} /><br /><br />
        <input type="date" name="admission_date" onChange={handleChange} /><br /><br />
        <input type="date" name="discharge_date" onChange={handleChange} /><br /><br />
        <input name="claimed_amount" placeholder="Claimed Amount" onChange={handleChange} /><br /><br />

        <button>Create Claim</button>
      </form>
    </div>
  );
}