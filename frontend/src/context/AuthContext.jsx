import { createContext, useContext, useState } from "react";
import { loginUser, logoutUser } from "../api/authApi";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState({
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
    username: localStorage.getItem("username"),
    role: localStorage.getItem("role"),
  });

  const login = async (loginData) => {
    const data = await loginUser(loginData);

    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    setUser({
      access: data.access,
      refresh: data.refresh,
      username: localStorage.getItem("username"),
      role: localStorage.getItem("role"),
    });

    return data;
  };

  const logout = () => {
    logoutUser();

    setUser({
      access: null,
      refresh: null,
      username: null,
      role: null,
    });
  };

  const isAuthenticated = Boolean(user.access);

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}