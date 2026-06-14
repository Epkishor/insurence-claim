import api from "./axios";

export const getHumanReviews = async () => {
  const response = await api.get("/reviews/human-reviews/");
  return response.data;
};

export const createHumanReview = async (reviewData) => {
  const response = await api.post("/reviews/human-reviews/", reviewData);
  return response.data;
};

export const getHumanReviewById = async (id) => {
  const response = await api.get(`/reviews/human-reviews/${id}/`);
  return response.data;
};