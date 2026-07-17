import { useEffect, useState } from "react";

import Sidebar from "../components/sidebar/Sidebar";
import ChatBox from "../components/chat/ChatBox";
import ChatInput from "../components/chat/ChatInput";
import RepositoryImporter from "../components/repository/RepositoryImporter";
import FileExplorer from "../components/files/FileExplorer";
import FileViewer from "../components/files/FileViewer";
import ThemeToggle from "../components/theme/ThemeToggle";

import {
  streamQuestion,
  getProjectOverview,
  getArchitecture,
  getDependencyGraph,
  getSecurityAnalysis,
  getCodeReview,
  getPerformanceAnalysis,
  getDocumentation,
  getRepositoryHealth,
} from "../api/chat";

import {
  getRepositories,
  importRepository,
  deleteRepository,
  getRepositoryMap
} from "../api/repository";

import {
  getFiles,
  getFile,
} from "../api/files";

export default function Home() {
  const [chats, setChats] = useState(() => {
    return (
      JSON.parse(localStorage.getItem("chats")) || [
        {
          id: Date.now(),
          title: "New Chat",
          repository: "",
          messages: [],
        },
      ]
    );
  });

  const [currentChat, setCurrentChat] = useState(
    chats[0]?.id ?? Date.now()
  );

  const [loading, setLoading] = useState(false);

  const [repositories, setRepositories] = useState([]);
  const [repository, setRepository] = useState("");

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [fileContent, setFileContent] = useState(null);

  useEffect(() => {
    localStorage.setItem(
      "chats",
      JSON.stringify(chats)
    );
  }, [chats]);

  useEffect(() => {
    loadRepositories();
  }, []);

  useEffect(() => {
    const chat = chats.find(
      (c) => c.id === currentChat
    );

    if (!chat) return;

    if (chat.repository) {
      setRepository(chat.repository);
    }
  }, [currentChat]);

  const activeChat =
    chats.find((c) => c.id === currentChat) ??
    chats[0];

  const activeRepository =
    activeChat?.repository || repository;

  useEffect(() => {
    if (!activeRepository) return;

    async function loadFiles() {
      try {
        const data = await getFiles(
          activeRepository
        );

        setFiles(data);
        setSelectedFile("");
        setFileContent(null);
      } catch (err) {
        console.error(err);
      }
    }

    loadFiles();
  }, [activeRepository]);

  async function loadRepositories() {
    try {
      const repos = await getRepositories();

      setRepositories(repos);

      if (!repository && repos.length) {
        setRepository(repos[0]);
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function handleImport(url) {
    try {
      await importRepository(url);

      const repos =
        await getRepositories();

      setRepositories(repos);

      const importedRepo = url
        .replace(/\/$/, "")
        .split("/")
        .pop();

      setRepository(importedRepo);

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                repository: importedRepo,
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    }
  }

  async function handleDelete() {
    if (!activeRepository) return;

    if (
      !window.confirm(
        `Delete repository "${activeRepository}"?`
      )
    )
      return;

    try {
      await deleteRepository(
        activeRepository
      );

      const repos =
        await getRepositories();

      setRepositories(repos);

      if (repos.length) {
        setRepository(repos[0]);
      } else {
        setRepository("");
        setFiles([]);
        setSelectedFile("");
        setFileContent(null);

        setChats((prev) =>
          prev.map((chat) =>
            chat.id === currentChat
              ? {
                  ...chat,
                  repository: "",
                }
              : chat
          )
        );
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function handleFileSelect(path) {
    try {
      setSelectedFile(path);

      const file = await getFile(
        activeRepository,
        path
      );

      setFileContent(file);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleSourceClick(source) {
    await handleFileSelect(source.path);
  }

  async function handleExplainFile() {
    if (!selectedFile){
      alert("Please select a file from the Repository Explorer first.");
      return;
    }

    await handleSend(`Explain "${selectedFile}" in detail.
Include:
1. Purpose
2. Architecture
3. Functions
4. Security
5. Best Practices
6. Improvements`);
  }

  async function handleReviewFile() {
    if (!selectedFile){
      alert("Please select a file from the Repository Explorer first.");
      return;
    }

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: `🔍 Code Review: ${selectedFile}`,
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response = await getCodeReview(
        activeRepository,
        selectedFile
      );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleProjectOverview() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "📊 Generate Project Overview",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getProjectOverview(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSecurityAnalysis() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "🔒 Security Analysis",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getSecurityAnalysis(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handlePerformanceAnalysis() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "⚡ Performance Analysis",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getPerformanceAnalysis(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDocumentation() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "📖 Generate Documentation",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getDocumentation(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRepositoryHealth() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "❤️ Repository Health",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response = await getRepositoryHealth(
        activeRepository
      );

      const message = `
  # ❤️ Repository Health

  ## Overall Score
  **${response.overall_score}/10**

  | Category | Score |
  |----------|------:|
  | Architecture | ${response.architecture}/10 |
  | Security | ${response.security}/10 |
  | Performance | ${response.performance}/10 |
  | Code Quality | ${response.code_quality}/10 |
  | Documentation | ${response.documentation}/10 |

  ## Summary

  ${response.summary}

  ## Recommendations

  ${response.recommendations
    .map((r) => `- ${r}`)
    .join("\n")}
  `;

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: message,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleArchitecture() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "🏗 Generate Architecture Diagram",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getArchitecture(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRepositoryMap() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "🗺 Generate Repository Map",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getRepositoryMap(
          activeRepository
        );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDependencyGraph() {
    if (!activeRepository) return;

    setLoading(true);

    try {
      const userMessage = {
        role: "user",
        text: "🔗 Generate Dependency Graph",
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  userMessage,
                ],
              }
            : chat
        )
      );

      const response =
        await getDependencyGraph(
          activeRepository
        );

  const message =`${response.analysis}

  \`\`\`mermaid
  ${response.mermaid}
  \`\`\``;

  console.log("========== GENERATED GRAPH ==========");
  console.log({ message });
  console.log("========== END GENERATED GRAPH ==========");

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: message,
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleWelcomePrompt(prompt) {
    switch (prompt) {
      case "Explain the selected file":
        return handleExplainFile();

      case "Review this code for bugs":
        return handleReviewFile();

      case "Find security vulnerabilities":
        return handleSecurityAnalysis();

      case "Explain the project architecture":
        return handleArchitecture();

      case "Summarize this repository":
        return handleProjectOverview();

      case "Suggest performance improvements":
        return handlePerformanceAnalysis();

      default:
        return;
    }
  }

  async function handleSend(question) {
    if (!activeRepository) return;

    const history = activeChat.messages.map((m) => ({
      role: m.role,
      content: m.text,
    }));

    const userMessage = {
      role: "user",
      text: question,
    };

    setChats((prev) =>
      prev.map((chat) =>
        chat.id === currentChat
          ? {
              ...chat,
              title:
                chat.messages.length === 0
                  ? question.slice(0, 30)
                  : chat.title,
              messages: [...chat.messages, userMessage],
            }
          : chat
      )
    );

    setLoading(true);

    try {
      const assistantIndex =
        activeChat.messages.length + 1;

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: "",
                    sources: [],
                  },
                ],
              }
            : chat
        )
      );

      let streamed = "";

      await streamQuestion(
        activeRepository,
        question,
        history,
        selectedFile,
        (chunk) => {
          streamed += chunk;

          setChats((prev) =>
            prev.map((chat) =>
              chat.id === currentChat
                ? {
                    ...chat,
                    messages: chat.messages.map(
                      (msg, idx) =>
                        idx === assistantIndex
                          ? {
                              ...msg,
                              text: streamed,
                            }
                          : msg
                    ),
                  }
                : chat
            )
          );
        }
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    const chat = {
      id: Date.now(),
      title: "New Chat",
      repository: activeRepository,
      messages: [],
    };

    setChats((prev) => [chat, ...prev]);
    setCurrentChat(chat.id);
  }

  function handleDeleteChat(chatId) {
    if (!window.confirm("Delete this chat?"))
      return;

    const updatedChats = chats.filter(
      (chat) => chat.id !== chatId
    );

    if (updatedChats.length === 0) {
      const chat = {
        id: Date.now(),
        title: "New Chat",
        repository: "",
        messages: [],
      };

      setChats([chat]);
      setCurrentChat(chat.id);
      return;
    }

    setChats(updatedChats);

    if (chatId === currentChat) {
      setCurrentChat(updatedChats[0].id);
    }
  }

  return (
    <div className="flex h-screen bg-slate-100 transition-colors dark:bg-slate-900">
      <Sidebar
        chats={chats}
        currentChat={currentChat}
        onSelect={setCurrentChat}
        onNewChat={newChat}
        onDelete={handleDeleteChat}
      />

      <div className="flex flex-1 flex-col">
        <header className="border-b border-slate-300 bg-white p-5 dark:border-slate-700 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              AI DevOps Assistant
            </h1>

            <ThemeToggle />
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-3">
            <select
              value={activeRepository}
              onChange={(e) => {
                const repo = e.target.value;

                setRepository(repo);

                setChats((prev) =>
                  prev.map((chat) =>
                    chat.id === currentChat
                      ? {
                          ...chat,
                          repository: repo,
                        }
                      : chat
                  )
                );
              }}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            >
              {repositories.map((repo) => (
                <option
                  key={repo}
                  value={repo}
                >
                  {repo}
                </option>
              ))}
            </select>

            <button
              onClick={handleProjectOverview}
              disabled={
                !activeRepository || loading
              }
              className="rounded-lg bg-violet-600 px-4 py-2 text-white hover:bg-violet-700 disabled:opacity-50"
            >
              📊 Project Overview
            </button>
            
            <button
              onClick={handleRepositoryHealth}
              disabled={!activeRepository || loading}
              className="rounded-lg bg-pink-600 px-4 py-2 text-white hover:bg-pink-700 disabled:opacity-50"
            >
              ❤️ Repository Health
            </button>
            
            <button
              onClick={handleDocumentation}
              disabled={!activeRepository || loading}
              className="rounded-lg bg-purple-600 px-4 py-2 text-white hover:bg-purple-700 disabled:opacity-50"
            >
              📖 Documentation
            </button>

            <button
              onClick={handleRepositoryMap}
              disabled={
                !activeRepository || loading
              }
              className="rounded-lg bg-cyan-600 px-4 py-2 text-white hover:bg-cyan-700 disabled:opacity-50"
            >
              🗺 Repository Map
            </button>

            <button
              onClick={handleDependencyGraph}
              disabled={
                !activeRepository || loading
              }
              className="rounded-lg bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700 disabled:opacity-50"
            >
              🔗 Dependency Graph
            </button>

            <button
              onClick={handleArchitecture}
              disabled={
                !activeRepository || loading
              }
              className="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:opacity-50"
            >
              🏗 Architecture
            </button>

            <button
              onClick={handleDelete}
              disabled={
                !activeRepository || loading
              }
              className="rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700 disabled:opacity-50"
            >
              Delete Repository
            </button>
          </div>

          <div className="mt-4">
            <RepositoryImporter
              onImport={handleImport}
            />
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          <div className="w-72 border-r border-slate-300 dark:border-slate-700">
            <FileExplorer
              files={files}
              selectedFile={selectedFile}
              onSelect={handleFileSelect}
            />
          </div>

          <div className="w-1/2 border-r border-slate-300 dark:border-slate-700">
            <FileViewer
              file={fileContent}
              onExplain={handleExplainFile}
              onReview={handleReviewFile}
            />
          </div>

          <div className="flex flex-1 flex-col">
            <ChatBox
              messages={activeChat.messages}
              onSourceClick={handleSourceClick}
              onPromptClick={handleWelcomePrompt}
            />

            <ChatInput
              onSend={handleSend}
              loading={loading}
            />
          </div>
        </div>
      </div>
    </div>
  );
}