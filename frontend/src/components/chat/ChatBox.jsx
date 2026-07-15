import { useEffect, useRef } from "react";

import Message from "./Message";
import WelcomeScreen from "./WelcomeScreen";

export default function ChatBox({
  messages,
  onSourceClick,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  if (messages.length === 0) {
    return <WelcomeScreen />;
  }

  return (
    <div className="flex-1 overflow-y-auto bg-slate-100 p-6 transition-colors dark:bg-slate-950">
      {messages.map((message, index) => (
        <Message
          key={index}
          role={message.role}
          text={message.text}
          sources={message.sources}
          onSourceClick={onSourceClick}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}