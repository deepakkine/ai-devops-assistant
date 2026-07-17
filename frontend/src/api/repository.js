import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

export async function getRepositories() {
  const response = await api.get("/repositories");
  return response.data;
}

export async function importRepository(
  githubUrl
) {
  const response = await api.post(
    "/repositories/import",
    {
      github_url: githubUrl,
    }
  );

  return response.data;
}

export async function getRepositoryMap(
  repository
) {
  const response = await api.get(
    `/repositories/${repository}/map`
  );

  return response.data;
}

export async function deleteRepository(
  repository
) {
  await api.delete(
    `/repositories/${repository}`
  );
}