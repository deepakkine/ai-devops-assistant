import CodeBlock from "../chat/CodeBlock";

export default function FileViewer({
  file,
  onExplain,
  onReview,
}) {
  if (!file) {
    return (
      <div className="flex h-full items-center justify-center bg-slate-50 transition-colors dark:bg-slate-900">
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-sm dark:border-slate-700 dark:bg-slate-800">
          <div className="mb-4 text-6xl">📄</div>

          <h2 className="mb-2 text-xl font-semibold text-slate-900 dark:text-white">
            No File Selected
          </h2>

          <p className="max-w-sm text-slate-500 dark:text-slate-400">
            Choose a file from the Repository Explorer to view,
            explain, or review its contents.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col bg-slate-50 transition-colors dark:bg-slate-900">
      <div className="sticky top-0 flex items-center justify-between border-b border-slate-200 bg-white px-5 py-4 dark:border-slate-700 dark:bg-slate-900">
        <div>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
            📄 {file.path}
          </h2>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Repository File
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onExplain}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
          >
            ✨ Explain
          </button>

          <button
            onClick={onReview}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-emerald-700"
          >
            🔍 Review Code
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-5">
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-800">
          <CodeBlock language="text">
            {file.content}
          </CodeBlock>
        </div>
      </div>
    </div>
  );
}