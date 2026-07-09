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

  const [loading, setLoading] = useState(false);

  async function sendMessage(text) {
    if (text.trim() === "" || loading) return;

    setLoading(true);

    // User Message + Typing
    setMessages((prev) => [
      ...prev,
      {
        text,
        sender: "user",
      },
      {
        text: "🤖 Typing...",
        sender: "bot",
      },
    ]);

    try {
      const response = await API.post("/chat", {
        message: text,
      });

      setMessages((prev) => {
        const updated = [...prev];

        // Remove Typing...
        updated.pop();

        // Add Bot Reply
        updated.push({
          text: response.data.reply,
          sender: "bot",
        });

        return updated;
      });

    } catch (error) {
  console.log("Full Error:", error);

  if (error.response) {
    console.log("Status:", error.response.status);
    console.log("Data:", error.response.data);
  } else {
    console.log("Message:", error.message);
  }

  setMessages((prev) => [
    ...prev,
    {
      text: "❌ " + (error.response?.data?.detail || error.message),
      sender: "bot",
    },
  ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <Header />

      <div className="main-content">
        <Sidebar />

        <div className="chat-section">
          <ChatBox messages={messages} />

          <InputBox
            sendMessage={sendMessage}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default Home;