import { useState } from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import API from "../services/api";

function Home() {
  const [messages, setMessages] = useState([
    {
      text: "👋 Hello! Welcome to AI Customer Support.",
      sender: "bot",
    },
    {
      text: "How can I help you today?",
      sender: "bot",
    },
  ]);

  async function sendMessage(text) {
    if (text.trim() === "") return;

    // User Message
    const userMessage = {
      text,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await API.post("/chat", {
        message: text,
      });

      const botMessage = {
        text: response.data.reply,
        sender: "bot",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("API Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          text: "❌ Backend connection failed.",
          sender: "bot",
        },
      ]);
    }
  }

  return (
    <div className="app">
      <Header />

      <div className="main-content">
        <Sidebar />

        <div className="chat-section">
          <ChatBox messages={messages} />
          <InputBox sendMessage={sendMessage} />
        </div>
      </div>
    </div>
  );
}

export default Home;