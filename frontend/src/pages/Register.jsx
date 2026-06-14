import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "HOSPITAL_STAFF",
  });

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await API.post("/users/register/", form);
    navigate("/");
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Username" onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <br /><br />
        <input placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <br /><br />
        <input type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <br /><br />
        <select onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="HOSPITAL_STAFF">Hospital Staff</option>
          <option value="INSURANCE_OFFICER">Insurance Officer</option>
          <option value="REVIEWER">Reviewer</option>
          <option value="ADMIN">Admin</option>
        </select>
        <br /><br />
        <button>Register</button>
      </form>
    </div>
  );
}