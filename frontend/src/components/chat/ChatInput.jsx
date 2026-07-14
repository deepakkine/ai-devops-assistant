import { useState } from "react";

export default function ChatInput({ onSend, loading }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    onSend(question);
    setQuestion("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-3 p-4 border-t border-slate-700"
    >
      <input
        className="flex-1 rounded-lg bg-slate-800 p-3 outline-none"
        placeholder="Ask anything about your infrastructure..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        disabled={loading}
      />

      <button
        className="rounded-lg bg-blue-600 px-6 py-3 hover:bg-blue-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Thinking..." : "Send"}
      </button>
    </form>
  );
}