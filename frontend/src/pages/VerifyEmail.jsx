import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import API from "../api";
import Turnstile from "../components/Turnstile";

export default function VerifyEmail() {
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state?.email || "";

  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [cooldown, setCooldown] = useState(0);
  const [resendToken, setResendToken] = useState("");
  const resendTurnstileRef = useRef(null);

  useEffect(() => {
    if (cooldown <= 0) return;
    const timer = setInterval(() => setCooldown((c) => c - 1), 1000);
    return () => clearInterval(timer);
  }, [cooldown]);

  const handleVerify = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    if (code.length !== 6) return setError("Enter the 6-digit code.");

    try {
      setLoading(true);
      await API.post("/users/verify-email/", { email, code });
      navigate("/", { state: { verified: true } });
    } catch (err) {
      setError(
        err.response?.data?.non_field_errors?.[0] ||
        err.response?.data?.email?.[0] ||
        "Invalid or expired code."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError("");
    setMessage("");
    if (!resendToken) return setError("Please complete the verification check.");

    try {
      await API.post("/users/resend-otp/", { email, turnstile_token: resendToken });
      setMessage("New code sent.");
      setCooldown(60);
    } catch (err) {
      setError(err.response?.data?.email?.[0] || "Could not resend code.");
    } finally {
      resendTurnstileRef.current?.reset();
      setResendToken("");
    }
  };

  if (!email) {
    return (
      <main className="auth-page">
        <p>No email to verify. <Link to="/register">Go back to registration</Link>.</p>
      </main>
    );
  }

  return (
    <main className="auth-page verify-page">
      <section className="register-shell">
        <div className="auth-card register-card">
          <h1>Verify your email</h1>
          <p>Enter the 6-digit code sent to <strong>{email}</strong></p>

          {error && <div className="auth-error" role="alert">{error}</div>}
          {message && <div className="auth-success" role="status">{message}</div>}

          <form onSubmit={handleVerify} className="auth-form">
            <div className="auth-field">
              <label htmlFor="code">Verification Code</label>
              <input
                id="code"
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                placeholder="000000"
                inputMode="numeric"
                maxLength={6}
              />
            </div>

            <button className="auth-submit" disabled={loading}>
              {loading ? "Verifying..." : "Verify Email"}
            </button>

            <div className="auth-field">
              <Turnstile ref={resendTurnstileRef} onVerify={setResendToken} action="resend_otp" />
            </div>

            <button
              type="button"
              className="auth-create"
              onClick={handleResend}
              disabled={cooldown > 0 || !resendToken}
            >
              {cooldown > 0 ? `Resend code in ${cooldown}s` : "Resend code"}
            </button>
          </form>
        </div>
      </section>
    </main>
  );
}