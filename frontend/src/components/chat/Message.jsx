import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import CodeBlock from "./CodeBlock";

export default function Message({
  role,
  text,
  sources = [],
  onSourceClick,
}) {
  return (
    <div
      className={`mb-6 flex ${
        role === "user"
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-4xl rounded-2xl px-5 py-4 shadow-lg ${
          role === "user"
            ? "bg-blue-600 text-white"
            : "bg-white text-slate-800 dark:bg-slate-800 dark:text-slate-100"
        }`}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code(props) {
              const {
                inline,
                className,
                children,
              } = props;

              const language =
                className?.replace(
                  "language-",
                  ""
                ) || "text";

              if (!inline) {
                return (
                  <CodeBlock language={language}>
                    {String(children).replace(
                      /\n$/,
                      ""
                    )}
                  </CodeBlock>
                );
              }

              return (
                <code className="rounded bg-slate-200 px-1 py-0.5 text-pink-600 dark:bg-slate-900 dark:text-pink-400">
                  {children}
                </code>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>

        {role === "assistant" &&
          sources.length > 0 && (
            <div className="mt-6 border-t border-slate-200 pt-4 dark:border-slate-700">
              <h4 className="mb-2 text-sm font-semibold text-slate-500 dark:text-slate-300">
                📄 Sources
              </h4>

              <div className="space-y-2">
                {sources.map(
                  (source, index) => (
                    <button
                      key={index}
                      onClick={() =>
                        onSourceClick?.(
                          source
                        )
                      }
                      className="block w-full rounded-lg bg-slate-100 px-3 py-2 text-left text-sm text-slate-700 transition hover:bg-slate-200 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-700"
                    >
                      📄 {source.path}
                    </button>
                  )
                )}
              </div>
            </div>
          )}
      </div>
    </div>
  );
}