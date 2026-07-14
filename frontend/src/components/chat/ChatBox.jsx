import { useEffect, useRef } from "react";

import Message from "./Message";

export default function ChatBox({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-6">
      {messages.map((message, index) => (
        <Message
          key={index}
          role={message.role}
          text={message.text}
          sources={message.sources}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}