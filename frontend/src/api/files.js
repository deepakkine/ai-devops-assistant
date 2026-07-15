import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

export async function getFiles(repository) {
  const response = await api.get(`/files/${repository}`);
  return response.data;
}

export async function getFile(repository, path) {
  const response = await api.get(`/file/${repository}`, {
    params: {
      path,
    },
  });

  return response.data;
}