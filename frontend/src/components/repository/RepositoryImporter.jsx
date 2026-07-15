import { useState } from "react";

export default function RepositoryImporter({
  onImport,
}) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleImport() {
    const repositoryUrl = url.trim();

    if (!repositoryUrl) return;

    try {
      setLoading(true);

      await onImport(repositoryUrl);

      setUrl("");
    } catch (err) {
      console.error("Repository import failed:", err);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      handleImport();
    }
  }

  return (
    <div className="mt-5 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-colors dark:border-slate-700 dark:bg-slate-900">
      <h3 className="mb-3 text-lg font-semibold text-slate-900 dark:text-white">
        📦 Import Repository
      </h3>

      <div className="flex gap-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="https://github.com/owner/repository"
          disabled={loading}
          className="flex-1 rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400 dark:focus:ring-blue-900"
        />

        <button
          onClick={handleImport}
          disabled={loading || !url.trim()}
          className="flex min-w-[130px] items-center justify-center rounded-xl bg-blue-600 px-6 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <svg
                className="h-5 w-5 animate-spin"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  opacity="0.3"
                />
                <path
                  d="M22 12a10 10 0 0 1-10 10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
              </svg>

              Importing...
            </div>
          ) : (
            "Import"
          )}
        </button>
      </div>

      <p className="mt-3 text-sm text-slate-500 dark:text-slate-400">
        Paste any public GitHub repository URL to index it with AI.
      </p>
    </div>
  );
}