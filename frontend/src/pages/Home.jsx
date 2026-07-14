import { useEffect, useState } from "react";

import Sidebar from "../components/sidebar/Sidebar";
import ChatBox from "../components/chat/ChatBox";
import ChatInput from "../components/chat/ChatInput";

import { askQuestion } from "../api/chat";

export default function Home() {
  const [chats, setChats] = useState(() => {
    return JSON.parse(localStorage.getItem("chats")) || [
      {
        id: Date.now(),
        title: "New Chat",
        messages: [],
      },
    ];
  });

  const [currentChat, setCurrentChat] = useState(chats[0].id);

  const [loading, setLoading] = useState(false);

  const [repository] = useState("aws-three-tier-devsecops-platform");

  useEffect(() => {
    localStorage.setItem("chats", JSON.stringify(chats));
  }, [chats]);

  const activeChat =
    chats.find((c) => c.id === currentChat) ?? chats[0];

  async function handleSend(question) {
    const history = activeChat.messages.map((m) => ({
      role: m.role,
      content: m.text,
    }));

    const userMessage = {
      role: "user",
      text: question,
    };

    setChats((prev) =>
      prev.map((chat) =>
        chat.id === currentChat
          ? {
              ...chat,
              title:
                chat.messages.length === 0
                  ? question.slice(0, 30)
                  : chat.title,
              messages: [...chat.messages, userMessage],
            }
          : chat
      )
    );

    setLoading(true);

    try {
      const response = await askQuestion(
        repository,
        question,
        history 
      );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    text: response.answer,
                    sources: response.sources ?? [],
                  },
                ],
              }
            : chat
        )
      );
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    const chat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setChats((prev) => [chat, ...prev]);
    setCurrentChat(chat.id);
  }

  return (
    <div className="flex h-screen bg-slate-900">
      <Sidebar
        chats={chats}
        currentChat={currentChat}
        onSelect={setCurrentChat}
        onNewChat={newChat}
      />

      <div className="flex flex-1 flex-col">
        <header className="border-b border-slate-700 p-5">
         <h1 className="text-2xl font-bold text-white">
            AI DevOps Assistant
         </h1>

         <p className="text-sm text-slate-400">
            Repository: {repository}
         </p>
        </header>

        <ChatBox messages={activeChat.messages} />

        <ChatInput
          onSend={handleSend}
          loading={loading}
        />
      </div>
    </div>
  );
}