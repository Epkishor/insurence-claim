import { Link, useLocation, useNavigate } from "react-router-dom";
import { logoutUser } from "../api/authApi";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  if (location.pathname === "/" || location.pathname === "/register") {
    return null;
  }

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  return (
    <nav style={styles.navbar}>
      <h3 style={styles.logo}>Insurance Claim</h3>

      <div>
        <Link style={styles.link} to="/dashboard">Dashboard</Link>
        <Link style={styles.link} to="/patients/create">Create Patient</Link>
        <Link style={styles.link} to="/claims/create">Create Claim</Link>
        <Link style={styles.link} to="/claims">Claims</Link>
        <Link style={styles.link} to="/profile">Profile</Link>

        <button style={styles.button} onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    background: "#0f172a",
    color: "white",
    padding: "14px 20px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  logo: {
    margin: 0,
  },
  link: {
    color: "white",
    marginRight: 15,
    textDecoration: "none",
  },
  button: {
    background: "#ef4444",
    color: "white",
    border: "none",
    padding: "8px 12px",
    cursor: "pointer",
  },
};
