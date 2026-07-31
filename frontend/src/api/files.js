import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
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