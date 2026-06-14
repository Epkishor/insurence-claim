import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      <Link style={styles.link} to="/dashboard">Dashboard</Link>
      <Link style={styles.link} to="/patients/create">Create Patient</Link>
      <Link style={styles.link} to="/claims/create">Create Claim</Link>
      <Link style={styles.link} to="/claims">All Claims</Link>
      <Link style={styles.link} to="/profile">Profile</Link>
    </aside>
  );
}

const styles = {
  sidebar: {
    width: 220,
    minHeight: "100vh",
    background: "#1e293b",
    padding: 20,
    display: "flex",
    flexDirection: "column",
  },
  link: {
    color: "white",
    textDecoration: "none",
    marginBottom: 15,
  },
};