import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import CopyButton from "../common/CopyButton";

export default function CodeBlock({
  language,
  children,
}) {
  return (
    <div className="my-5 overflow-hidden rounded-xl border border-slate-700">

      <div className="flex items-center justify-between bg-slate-800 px-4 py-2">

        <span className="text-sm text-gray-300">
          {language || "text"}
        </span>

        <CopyButton text={children} />

      </div>

      <SyntaxHighlighter
        language={language}
        style={atomDark}
        customStyle={{
          margin: 0,
          borderRadius: 0,
        }}
      >
        {children}
      </SyntaxHighlighter>

    </div>
  );
}