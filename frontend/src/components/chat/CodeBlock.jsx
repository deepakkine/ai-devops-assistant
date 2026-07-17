let renderVersion = 0;

import { useEffect, useMemo, useRef, useState } from "react";

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
  const containerRef = useRef(null);

  const svgContentRef = useRef("");

  useEffect(() => {
    let cancelled = false;

    async function renderDiagram() {
      if (!containerRef.current) return;

      const currentRender = ++renderVersion;

      containerRef.current.innerHTML = "";

      const code = chart.trim();

      // Only attempt to render valid Mermaid diagrams.
      if (
        !/^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|journey)/.test(
          code
        )
      ) {
        containerRef.current.innerHTML = `
  <pre style="padding:16px;color:red;">
  Invalid Mermaid diagram.
  </pre>`;
        return;
      }

      try {
        const { svg } = await mermaid.render(
          `mermaid-${currentRender}`,
          code
        );

        if (
          cancelled ||
          currentRender !== renderVersion ||
          !containerRef.current
        ) {
          return;
        }

        svgContentRef.current = svg;

        containerRef.current.innerHTML = svg;

        const svgElement =
          containerRef.current.querySelector("svg");

        if (svgElement) {
          svgElement.removeAttribute("width");
          svgElement.removeAttribute("height");

          svgElement.style.maxWidth = "100%";
          svgElement.style.height = "auto";
          svgElement.style.display = "block";
          svgElement.style.margin = "0 auto";
        }
      } catch (err) {
        if (!cancelled && containerRef.current) {
          containerRef.current.innerHTML = `
  <pre style="padding:16px;color:red;white-space:pre-wrap;">
  ${err.message}
  </pre>`;
        }
      }
    }

    renderDiagram();

    return () => {
      cancelled = true;
    };
  }, [chart]);

  function downloadSVG() {
    const blob = new Blob([svgContentRef.current], {
      type: "image/svg+xml",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "diagram.svg";

    a.click();

    URL.revokeObjectURL(url);
  }

  function downloadMermaid() {
    const blob = new Blob([chart], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "diagram.mmd";

    a.click();

    URL.revokeObjectURL(url);
  }

  function downloadPNG() {
    const blob = new Blob([svgContentRef.current], {
      type: "image/svg+xml",
    });

    const url = URL.createObjectURL(blob);

    const img = new Image();

    img.onload = () => {
      const canvas =
        document.createElement("canvas");

      canvas.width = img.width;
      canvas.height = img.height;

      const ctx = canvas.getContext("2d");

      ctx.drawImage(img, 0, 0);

      URL.revokeObjectURL(url);

      const png = canvas.toDataURL(
        "image/png"
      );

      const a =
        document.createElement("a");

      a.href = png;
      a.download = "diagram.png";

      a.click();
    };

    img.src = url;
  }

  return (
    <>
      <div className="flex justify-end gap-2 border-b border-slate-200 bg-slate-100 px-4 py-2 dark:border-slate-700 dark:bg-slate-800">
        <button
          onClick={downloadSVG}
          className="rounded bg-blue-600 px-3 py-1 text-xs text-white hover:bg-blue-700"
        >
          SVG
        </button>

        <button
          onClick={downloadPNG}
          className="rounded bg-green-600 px-3 py-1 text-xs text-white hover:bg-green-700"
        >
          PNG
        </button>

        <button
          onClick={downloadMermaid}
          className="rounded bg-purple-600 px-3 py-1 text-xs text-white hover:bg-purple-700"
        >
          Mermaid
        </button>
      </div>

      <div className="overflow-auto rounded-lg bg-white p-6 dark:bg-slate-900">
        <div
          ref={containerRef}
          style={{
            minHeight: "250px",
          }}
        />
      </div>
    </>
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

  const code =
    typeof children === "string"
      ? children.trim()
      : String(children).trim();

  if (language === "mermaid") {
    return (
      <div className="my-5 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-100 px-4 py-3 dark:border-slate-700 dark:bg-slate-800">
          <span className="rounded bg-violet-600 px-2 py-1 text-xs font-semibold uppercase text-white">
            Mermaid Diagram
          </span>

          <CopyButton text={code} />
        </div>

        <MermaidDiagram chart={code} />
      </div>
    );
  }

  return (
    <div className="my-5 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <div className="flex items-center justify-between border-b border-slate-200 bg-slate-100 px-4 py-3 dark:border-slate-700 dark:bg-slate-800">
        <span className="rounded bg-slate-200 px-2 py-1 text-xs font-semibold uppercase dark:bg-slate-700">
          {language || "text"}
        </span>

        <CopyButton text={code} />
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
        }}
        showLineNumbers
        wrapLongLines
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}