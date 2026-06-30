import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [form, setForm] = useState({ username: "", password: "", remember: false });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, checked, type } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.username.trim()) return setError("Email or username is required.");
    if (!form.password.trim()) return setError("Password is required.");

    try {
      setLoading(true);
      await login({ username: form.username, password: form.password });

      if (form.remember) {
        localStorage.setItem("rememberLogin", "true");
      } else {
        localStorage.removeItem("rememberLogin");
      }

      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password. Please check your details and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <header className="auth-header">
        <div className="auth-brand">
          <Logo />
          <div>
            <h1>Insurance Claim</h1>
            <p>Intelligent Health Claim Processing</p>
          </div>
        </div>

        <a href="mailto:insurifyx.app@gmail.com" className="auth-support-link">
          Help / Support
        </a>
      </header>

      <section className="auth-shell">
        <div className="auth-info-panel">
          <div className="auth-chip">AI-powered claim verification for hospitals and insurers</div>

          <h2>Secure, explainable, and faster health insurance claim processing.</h2>

          <p className="auth-lead">
            A modern platform for hospitals, insurance companies, and claim officers to submit,
            verify, review, and approve claims with intelligent automation.
          </p>

      

          <div className="auth-illustration-card">
            <div className="auth-illustration-icon">
              <Logo small />
            </div>
            <div>
              <h3>Enterprise claim intelligence</h3>
              <p>
                Document analysis, policy eligibility, fraud risk scoring, and explainable decisions.
              </p>
            </div>
          </div>

          <div className="auth-flow-card">
            <div className="auth-flow-step active">Submit</div>
            <div className="auth-flow-line"></div>
            <div className="auth-flow-step active">Verify</div>
            <div className="auth-flow-line"></div>
            <div className="auth-flow-step">Review</div>
            <div className="auth-flow-line"></div>
            <div className="auth-flow-step">Approve</div>
          </div>
        </div>

        <div className="auth-form-wrap">
          <div className="auth-card">
            <div className="auth-card-header">
              <p>Welcome back</p>
              <h2>Sign in to your account</h2>
              <span>Manage claims, documents, reviews, and final decisions.</span>
            </div>

            {error && (
              <div className="auth-error" role="alert">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="auth-field">
                <label htmlFor="username">Email or Username</label>
                <div className="auth-input-group">
                  <span aria-hidden="true">
                    <UserIcon />
                  </span>
                  <input
                    id="username"
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    placeholder="claimofficer@hospital.com"
                    autoComplete="username"
                  />
                </div>
              </div>

              <div className="auth-field">
                <label htmlFor="password">Password</label>
                <div className="auth-input-group">
                  <span aria-hidden="true">
                    <LockIcon />
                  </span>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    value={form.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((prev) => !prev)}
                    className="auth-show-password"
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </div>

              <div className="auth-options">
                <label>
                  <input
                    name="remember"
                    type="checkbox"
                    checked={form.remember}
                    onChange={handleChange}
                  />
                  Remember me
                </label>

                <a href="#">Forgot password?</a>
              </div>

              <button className="auth-submit" disabled={loading}>
                {loading ? "Signing in..." : "Sign In"}
              </button>

              <Link to="/register" className="auth-create">
                Create Account
              </Link>
            </form>
          </div>
        </div>
      </section>
    </main>
  );
}

function Logo({ small = false }) {
  return (
    <svg
      className={small ? "auth-logo-small" : "auth-logo"}
      viewBox="0 0 64 64"
      role="img"
      aria-label="Insurance Claim logo"
    >
      <defs>
        <linearGradient id="logoGradient" x1="10" x2="54" y1="8" y2="58">
          <stop stopColor="#2563EB" />
          <stop offset="1" stopColor="#06B6D4" />
        </linearGradient>
      </defs>
      <path
        d="M32 5 52 13v15c0 14.4-8.1 25.1-20 30.5C20.1 53.1 12 42.4 12 28V13L32 5Z"
        fill="url(#logoGradient)"
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
      <circle cx="45" cy="18" r="2.4" fill="#DBEAFE" />
      <circle cx="49" cy="25" r="2.2" fill="#DBEAFE" />
      <path d="M45 18 49 25" stroke="#DBEAFE" strokeWidth="1.7" />
    </svg>
  );
}

function Stat({ value, label }) {
  return (
    <div className="auth-stat">
      <p>{value}</p>
      <span>{label}</span>
    </div>
  );
}

function UserIcon() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M20 21a8 8 0 0 0-16 0" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}

function LockIcon() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="4" y="11" width="16" height="10" rx="2" />
      <path d="M8 11V8a4 4 0 0 1 8 0v3" />
    </svg>
  );
}
