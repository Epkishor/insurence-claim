import api from "./axios";

export const loginUser = async (loginData) => {
  const response = await api.post("/token/", loginData);
  return response.data;
};

export const refreshToken = async (refreshData) => {
  const response = await api.post("/token/refresh/", refreshData);
  return response.data;
};

export const registerUser = async (userData) => {
  const response = await api.post("/users/register/", userData);
  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  localStorage.removeItem("role");
};