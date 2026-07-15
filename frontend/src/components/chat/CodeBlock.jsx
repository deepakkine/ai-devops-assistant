import { useEffect, useMemo, useRef } from "react";

import mermaid from "mermaid";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  atomDark,
  oneLight,
} from "react-syntax-highlighter/dist/esm/styles/prism";

import CopyButton from "../common/CopyButton";
import { useTheme } from "../../context/ThemeContext";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
});

function MermaidDiagram({ chart }) {
  const ref = useRef(null);

  useEffect(() => {
    async function render() {
      if (!ref.current) return;

      try {
        const id = `mermaid-${Date.now()}`;

        const { svg } = await mermaid.render(
          id,
          chart
        );

        ref.current.innerHTML = svg;
      } catch (err) {
        ref.current.innerHTML = `
          <pre style="color:red;white-space:pre-wrap;">
${err.message}
          </pre>
        `;
      }
    }

    render();
  }, [chart]);

  return (
    <div
      ref={ref}
      className="overflow-auto rounded-lg bg-white p-4 dark:bg-slate-900"
    />
  );
}

export default function CodeBlock({
  language,
  children,
}) {
  const { theme } = useTheme();

  const style = useMemo(
    () =>
      theme === "dark"
        ? atomDark
        : oneLight,
    [theme]
  );

  if (language === "mermaid") {
    return (
      <div className="my-5 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-100 px-4 py-3 dark:border-slate-700 dark:bg-slate-800">
          <span className="rounded-md bg-violet-600 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-white">
            Mermaid Diagram
          </span>

          <CopyButton text={children} />
        </div>

        <MermaidDiagram chart={children} />
      </div>
    );
  }

  return (
    <div className="my-5 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-colors dark:border-slate-700 dark:bg-slate-900">
      <div className="flex items-center justify-between border-b border-slate-200 bg-slate-100 px-4 py-3 dark:border-slate-700 dark:bg-slate-800">
        <span className="rounded-md bg-slate-200 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-slate-700 dark:bg-slate-700 dark:text-slate-200">
          {language || "text"}
        </span>

        <CopyButton text={children} />
      </div>

      <SyntaxHighlighter
        language={language}
        style={style}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          background:
            theme === "dark"
              ? "#0f172a"
              : "#ffffff",
          fontSize: "14px",
        }}
        showLineNumbers
        wrapLongLines
      >
        {children}
      </SyntaxHighlighter>
    </div>
  );
}