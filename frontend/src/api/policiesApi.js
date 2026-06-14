import api from "./axios";

export const getInsuranceCompanies = async () => {
  const response = await api.get("/policies/companies/");
  return response.data;
};

export const createInsuranceCompany = async (companyData) => {
  const response = await api.post("/policies/companies/", companyData);
  return response.data;
};

export const getPolicies = async () => {
  const response = await api.get("/policies/policies/");
  return response.data;
};

export const createPolicy = async (policyData) => {
  const response = await api.post("/policies/policies/", policyData);
  return response.data;
};

export const getPolicyClauses = async () => {
  const response = await api.get("/policies/clauses/");
  return response.data;
};

export const createPolicyClause = async (clauseData) => {
  const response = await api.post("/policies/clauses/", clauseData);
  return response.data;
};