import { useNavigate } from "react-router-dom";

export default function Profile() {
  const navigate = useNavigate();

  const username = localStorage.getItem("username") || "Logged In User";
  const role = localStorage.getItem("role") || "User";

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    navigate("/");
  };

  return (
    <div>
      <h2>Profile</h2>

      <div style={{ border: "1px solid #ccc", padding: 15, width: 350 }}>
        <p>
          <strong>Username:</strong> {username}
        </p>

        <p>
          <strong>Role:</strong> {role}
        </p>

        <p>
          <strong>Status:</strong> Logged in
        </p>

        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}