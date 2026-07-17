const API_URL = "http://127.0.0.1:8000/api/v1";

export async function askQuestion(
  repository,
  question,
  history = [],
  selectedFile = null
) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      repository,
      question,
      history,
      selected_file: selectedFile,
    }),
  });

  if (!response.ok) {
    throw new Error("Chat request failed");
  }

  return await response.json();
}

export async function streamQuestion(
  repository,
  question,
  history = [],
  selectedFile = null,
  onChunk
) {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      repository,
      question,
      history,
      selected_file: selectedFile,
    }),
  });

  if (!response.ok) {
    throw new Error("Streaming request failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    onChunk(decoder.decode(value));
  }
}

export async function getProjectOverview(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/project-overview/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate project overview"
    );
  }

  return await response.json();
}

export async function getArchitecture(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/architecture/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate architecture"
    );
  }

  return await response.json();
}

export async function getDependencyGraph(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/dependency-graph/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate dependency graph"
    );
  }

  return await response.json();
}

export async function getSecurityAnalysis(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/security-analysis/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate security analysis"
    );
  }

  return await response.json();
}

export async function getCodeReview(
  repository,
  filePath
) {
  const response = await fetch(
    `${API_URL}/chat/code-review/${repository}/${encodeURIComponent(filePath)}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate code review"
    );
  }

  return await response.json();
}

export async function getPerformanceAnalysis(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/performance-analysis/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate performance analysis"
    );
  }

  return await response.json();
}

export async function getDocumentation(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/documentation/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate documentation"
    );
  }

  return await response.json();
}

export async function getRepositoryHealth(
  repository
) {
  const response = await fetch(
    `${API_URL}/chat/repository-health/${repository}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate repository health"
    );
  }

  return await response.json();
}