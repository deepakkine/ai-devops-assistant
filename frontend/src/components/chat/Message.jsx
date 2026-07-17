import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import CodeBlock from "./CodeBlock";

import { jsPDF } from "jspdf";

export default function Message({
  role,
  text,
  sources = [],
  onSourceClick,
}) {

  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(text);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
}

function handleDownload() {
  const blob = new Blob([text], {
    type: "text/markdown",
  });

  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");

  a.href = url;
  const fileName = `${role}-report-${new Date()
    .toISOString()
    .slice(0, 10)}.md`;

  a.download = fileName;

  a.click();

  URL.revokeObjectURL(url);
}

function handlePDF() {
  const pdf = new jsPDF();

  const lines = pdf.splitTextToSize(
    text,
    180
  );

  pdf.text(lines, 10, 10);

  const fileName = `${role}-report-${new Date()
    .toISOString()
    .slice(0, 10)}.pdf`;

  pdf.save(fileName);
}

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
            pre({ children }) {
              return <>{children}</>;
            },

            code({
              inline,
              className,
              children,
              ...props
            }) {

              const match =
                /language-(\w+)/.exec(className || "");

              const language = match
                ? match[1]
                : "text";

              const code = String(children).replace(/\n$/, "");

              if (inline) {
                return (
                  <code {...props}>
                    {children}
                  </code>
                );
              }

              return (
                <CodeBlock language={language}>
                  {code}
                </CodeBlock>
              );
            }
          }}
        >
          {text}
        </ReactMarkdown>

        {role === "assistant" && (
          <div className="mt-4 flex justify-end gap-2">

            <button
              onClick={handleDownload}
              className="rounded-lg bg-emerald-600 px-3 py-2 text-sm text-white hover:bg-emerald-700"
            >
              📄 Markdown
            </button>

            <button
              onClick={handlePDF}
              className="rounded-lg bg-red-600 px-3 py-2 text-sm text-white hover:bg-red-700"
            >
              📕 PDF
            </button>

            <button
              onClick={handleCopy}
              className="rounded-lg bg-slate-700 px-3 py-2 text-sm text-white hover:bg-slate-800"
            >
              {copied ? "✅ Copied" : "📋 Copy"}
            </button>
          </div>
        )}

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