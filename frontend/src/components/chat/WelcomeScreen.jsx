export default function WelcomeScreen({ onPromptClick = () => {} }) {
  const prompts = [
    "Explain the selected file",
    "Review this code for bugs",
    "Find security vulnerabilities",
    "Explain the project architecture",
    "Summarize this repository",
    "Suggest performance improvements",
  ];

  return (
    <div className="flex h-full flex-col items-center justify-center px-8 text-center">
      <div className="mb-8 text-6xl">
        🤖
      </div>

      <h1 className="mb-3 text-4xl font-bold text-slate-900 dark:text-white">
        AI DevOps Assistant 🚀
      </h1>

      <p className="mb-10 max-w-2xl text-slate-600 dark:text-slate-400">
        Analyze repositories, review code, explain architecture,
        detect security issues, and get AI-powered insights.
      </p>

      <div className="grid w-full max-w-3xl gap-3 md:grid-cols-2">
        {prompts.map((prompt) => (
          <button
            key={prompt}
            type="button"
            onClick={() => onPromptClick(prompt)}
            className="rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:shadow-md hover:border-violet-500 hover:bg-violet-50 dark:border-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700"
          >
            <p className="font-medium text-slate-900 dark:text-white">
              {prompt}
            </p>
          </button>
        ))}
      </div>

      <p className="mt-10 text-sm text-slate-500 dark:text-slate-400">
        Select a repository and start chatting below.
      </p>
    </div>
  );
}