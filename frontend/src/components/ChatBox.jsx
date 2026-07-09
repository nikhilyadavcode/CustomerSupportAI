import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatBox({ messages }) {

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <main className="chat-box">

      {messages.map((msg, index) => (
        <Message
          key={index}
          text={msg.text}
          sender={msg.sender}
        />
      ))}

      <div ref={chatEndRef}></div>

    </main>
  );
}

export default ChatBox;