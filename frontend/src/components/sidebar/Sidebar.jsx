export default function Sidebar({
  chats,
  currentChat,
  onSelect,
  onNewChat,
  onDelete,
}) {
  return (
    <aside className="flex w-72 flex-col border-r border-slate-200 bg-white text-slate-900 transition-colors dark:border-slate-700 dark:bg-slate-950 dark:text-white">
      <div className="border-b border-slate-200 p-4 dark:border-slate-700">
        <button
          onClick={onNewChat}
          className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white shadow transition hover:bg-blue-700"
        >
          + New Chat
        </button>
      </div>

      <div className="flex-1 space-y-2 overflow-y-auto p-3">
        {chats.map((chat) => {
          const active = currentChat === chat.id;

          return (
            <div
              key={chat.id}
              className={`group flex items-center rounded-xl border transition ${
                active
                  ? "border-blue-500 bg-blue-50 shadow-sm dark:bg-slate-800"
                  : "border-transparent hover:border-slate-300 hover:bg-slate-100 dark:hover:border-slate-700 dark:hover:bg-slate-900"
              }`}
            >
              <button
                onClick={() => onSelect(chat.id)}
                className="flex-1 truncate px-4 py-3 text-left text-sm font-medium"
              >
                {chat.title}
              </button>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(chat.id);
                }}
                className="mr-2 rounded-lg p-2 text-slate-400 transition hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-900/40 dark:hover:text-red-400"
                title="Delete Chat"
              >
                🗑️
              </button>
            </div>
          );
        })}
      </div>
    </aside>
  );
}