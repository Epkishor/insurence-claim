import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

export default function CreatePatient() {
  const [form, setForm] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await API.post("/claims/patients/", form);
    navigate("/claims/create");
  };

  return (
    <div>
      <h2>Create Patient</h2>
      <form onSubmit={handleSubmit}>
        <input name="full_name" placeholder="Full Name" onChange={handleChange} /><br /><br />
        <input name="age" placeholder="Age" onChange={handleChange} /><br /><br />
        <input name="gender" placeholder="Gender" onChange={handleChange} /><br /><br />
        <input name="phone_number" placeholder="Phone Number" onChange={handleChange} /><br /><br />
        <textarea name="address" placeholder="Address" onChange={handleChange}></textarea><br /><br />
        <input name="insurance_number" placeholder="Insurance Number" onChange={handleChange} /><br /><br />
        <button>Create Patient</button>
      </form>
    </div>
  );
}