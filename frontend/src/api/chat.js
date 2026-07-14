import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

export const askQuestion = async (
  repository,
  question,
  history = []
) => {
  const response = await api.post("/chat", {
    repository,
    question,
    history,
  });

  return response.data;
};