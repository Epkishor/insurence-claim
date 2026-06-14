import api from "./axios";

export const getHospitals = async () => {
  const response = await api.get("/users/hospitals/");
  return response.data;
};

export const createHospital = async (hospitalData) => {
  const response = await api.post("/users/hospitals/", hospitalData);
  return response.data;
};

export const getProfiles = async () => {
  const response = await api.get("/users/profiles/");
  return response.data;
};

export const getProfileById = async (id) => {
  const response = await api.get(`/users/profiles/${id}/`);
  return response.data;
};