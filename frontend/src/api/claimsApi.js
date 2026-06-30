import api from "./axios";

export const getPatients = async () => {
  const response = await api.get("/claims/patients/");
  return response.data;
};

export const createPatient = async (patientData) => {
  const response = await api.post("/claims/patients/", patientData);
  return response.data;
};

export const getClaims = async () => {
  const response = await api.get("/claims/claims/");
  return response.data;
};

export const getClaimById = async (id) => {
  const response = await api.get(`/claims/claims/${id}/`);
  return response.data;
};

export const createClaim = async (claimData) => {
  const response = await api.post("/claims/claims/", claimData);
  return response.data;
};

export const processClaim = async (id) => {
  const response = await api.post(`/claims/claims/${id}/process/`);
  return response.data;
};

export const aiProcessClaim = async (id, aiOptions = {}) => {
  const response = await api.post(`/claims/claims/${id}/ai-process/`, aiOptions);
  return response.data;
};
