export default function Sidebar({
  chats,
  currentChat,
  onSelect,
  onNewChat,
}) {
  return (
    <aside className="w-72 border-r border-slate-700 bg-slate-950 text-white">
      <button
        onClick={onNewChat}
        className="m-4 w-[calc(100%-2rem)] rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-700"
      >
        + New Chat
      </button>

      <div className="px-4">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelect(chat.id)}
            className={`mb-2 w-full rounded-lg p-3 text-left ${
              currentChat === chat.id
                ? "bg-slate-700"
                : "hover:bg-slate-800"
            }`}
          >
            {chat.title}
          </button>
        ))}
      </div>
    </aside>
  );
}