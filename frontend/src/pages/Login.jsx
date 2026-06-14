import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await API.post("/token/", form);
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
    navigate("/dashboard");
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Username" onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <br /><br />
        <input type="password" placeholder="Password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <br /><br />
        <button>Login</button>
      </form>
      <p><Link to="/register">Create account</Link></p>
    </div>
  );
}