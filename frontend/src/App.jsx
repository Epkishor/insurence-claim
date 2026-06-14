import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import CreatePatient from "./pages/CreatePatient";
import CreateClaim from "./pages/CreateClaim";
import UploadDocuments from "./pages/UploadDocuments";
import ClaimList from "./pages/ClaimList";
import ClaimDetails from "./pages/ClaimDetails";
import ReviewClaim from "./pages/ReviewClaim";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <>
      <Navbar />

      <main className="main-container">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/patients/create"
            element={
              <ProtectedRoute>
                <CreatePatient />
              </ProtectedRoute>
            }
          />

          <Route
            path="/claims/create"
            element={
              <ProtectedRoute>
                <CreateClaim />
              </ProtectedRoute>
            }
          />

          <Route
            path="/claims"
            element={
              <ProtectedRoute>
                <ClaimList />
              </ProtectedRoute>
            }
          />

          <Route
            path="/claims/:id"
            element={
              <ProtectedRoute>
                <ClaimDetails />
              </ProtectedRoute>
            }
          />

          <Route
            path="/claims/:id/upload"
            element={
              <ProtectedRoute>
                <UploadDocuments />
              </ProtectedRoute>
            }
          />

          <Route
            path="/claims/:id/review"
            element={
              <ProtectedRoute>
                <ReviewClaim />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </>
  );
}