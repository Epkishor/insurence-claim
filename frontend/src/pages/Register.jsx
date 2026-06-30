import { useState, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api";
import Turnstile from "../components/Turnstile";

export default function Register() {
  const navigate = useNavigate();
  const turnstileRef = useRef(null);
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "HOSPITAL_STAFF",
  });
  const [turnstileToken, setTurnstileToken] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.username.trim()) return setError("Username is required.");
    if (!form.email.trim()) return setError("Email is required.");
    if (!form.password.trim()) return setError("Password is required.");
    if (form.password.length < 6) return setError("Password must be at least 6 characters.");
    if (!turnstileToken) return setError("Please complete the verification check.");

    try {
      setLoading(true);
      await API.post("/users/register/", { ...form, turnstile_token: turnstileToken });
      navigate("/verify-email", { state: { email: form.email } });
    } catch (err) {
      setError("Could not create account. Please check your details and try again.");
      turnstileRef.current?.reset();
      setTurnstileToken("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page register-page">
      <header className="auth-header">
        <div className="auth-brand">
          <RegisterLogo />
          <div>
            <h1>Insurance Claim</h1>
            <p>Intelligent Health Claim Processing</p>
          </div>
        </div>

        <Link to="/" className="auth-support-link">
          Back to Login
        </Link>
      </header>

      <section className="register-shell">
        <div className="auth-card register-card">
          <div className="auth-card-header register-card-header">
            <p>Create account</p>
            <h2>Register your account</h2>
            <span>Fill in your details to access the insurance claim platform.</span>
          </div>

          {error && (
            <div className="auth-error" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="auth-field">
              <label htmlFor="username">Username</label>
              <div className="auth-input-group">
                <span aria-hidden="true">#</span>
                <input
                  id="username"
                  name="username"
                  value={form.username}
                  onChange={handleChange}
                  placeholder="claimofficer"
                  autoComplete="username"
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="email">Email Address</label>
              <div className="auth-input-group">
                <span aria-hidden="true">@</span>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="claimofficer@hospital.com"
                  autoComplete="email"
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="password">Password</label>
              <div className="auth-input-group">
                <span aria-hidden="true">*</span>
                <input
                  id="password"
                  name="password"
                  type="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Create a strong password"
                  autoComplete="new-password"
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="role">User Role</label>
              <div className="auth-input-group">
                <span aria-hidden="true">Role</span>
                <select id="role" name="role" value={form.role} onChange={handleChange}>
                  <option value="HOSPITAL_STAFF">Hospital Staff</option>
                  <option value="INSURANCE_OFFICER">Insurance Officer</option>
                  <option value="REVIEWER">Reviewer</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>
            </div>

            <div className="auth-field">
              <Turnstile ref={turnstileRef} onVerify={setTurnstileToken} action="register" />
            </div>

            <button className="auth-submit" disabled={loading || !turnstileToken}>
              {loading ? "Creating account..." : "Create Account"}
            </button>

            <Link to="/" className="auth-create">
              Already have an account? Sign In
            </Link>
          </form>
        </div>
      </section>
    </main>
  );
}

function RegisterLogo() {
  return (
    <svg className="auth-logo" viewBox="0 0 64 64" role="img" aria-label="Insurance Claim logo">
      <defs>
        <linearGradient id="registerLogoGradient" x1="10" x2="54" y1="8" y2="58">
          <stop stopColor="#2563EB" />
          <stop offset="1" stopColor="#06B6D4" />
        </linearGradient>
      </defs>
      <path
        d="M32 5 52 13v15c0 14.4-8.1 25.1-20 30.5C20.1 53.1 12 42.4 12 28V13L32 5Z"
        fill="url(#registerLogoGradient)"
      />
      <path d="M29 20h6v9h9v6h-9v9h-6v-9h-9v-6h9v-9Z" fill="#FFFFFF" />
      <path
        d="m26.5 45.2 5.1 5.1L45.3 35.9"
        fill="none"
        stroke="#10B981"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="5"
      />
    </svg>
  );
}
