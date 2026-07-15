import { useRef, useState } from "react";

export default function ChatInput({
  onSend,
  loading,
}) {
  const [question, setQuestion] = useState("");

  const textareaRef = useRef(null);

  function resizeTextarea() {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      180
    )}px`;
  }

  function handleChange(e) {
    setQuestion(e.target.value);
    resizeTextarea();
  }

  function handleSubmit(e) {
    e.preventDefault();

    if (!question.trim() || loading) return;

    onSend(question.trim());

    setQuestion("");

    requestAnimationFrame(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    });
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-slate-200 bg-white p-5 transition-colors dark:border-slate-700 dark:bg-slate-900"
    >
      <div className="flex items-end gap-3">
        <textarea
          ref={textareaRef}
          rows={1}
          value={question}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={loading}
          placeholder="Ask anything about your repository..."
          className="max-h-44 min-h-[52px] flex-1 resize-none rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400 dark:focus:ring-blue-900"
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="flex h-[52px] items-center justify-center rounded-xl bg-blue-600 px-6 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
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

              Thinking...
            </div>
          ) : (
            "Send"
          )}
        </button>
      </div>

      <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
        Press <strong>Enter</strong> to send •{" "}
        <strong>Shift + Enter</strong> for a new line
      </p>
    </form>
  );
}