import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import CodeBlock from "./CodeBlock";

export default function Message({
  role,
  text,
  sources = [],
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
            : "bg-slate-800 text-gray-100"
        }`}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ className, children }) {
              const match = /language-(\w+)/.exec(className || "");

              if (match) {
                return (
                  <CodeBlock language={match[1]}>
                    {String(children).replace(/\n$/, "")}
                  </CodeBlock>
                );
              }

              return (
                <code className="rounded bg-slate-900 px-1 py-0.5 text-pink-400">
                  {children}
                </code>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>

        {role === "assistant" && sources.length > 0 && (
          <div className="mt-6 border-t border-slate-700 pt-4">
            <h4 className="mb-2 text-sm font-semibold text-slate-300">
              📄 Sources
            </h4>

            <div className="space-y-2">
              {sources.map((source, index) => (
                <div
                  key={index}
                  className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-slate-300"
                >
                  {source.path}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}