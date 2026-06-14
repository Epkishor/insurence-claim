import api from "./axios";

export const getClaimDocuments = async () => {
  const response = await api.get("/documents/claim-documents/");
  return response.data;
};

export const uploadClaimDocument = async (documentData) => {
  const response = await api.post("/documents/claim-documents/", documentData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getOCRResults = async () => {
  const response = await api.get("/documents/ocr-results/");
  return response.data;
};