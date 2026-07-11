import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";

import API from "../services/api";

function Home() {

  const navigate = useNavigate();

  const username = localStorage.getItem("name");

  const welcomeMessages = [
    {
      text: "👋 Hello! Welcome to AI Customer Support.",
      sender: "bot",
    },
    {
      text: "How can I help you today?",
      sender: "bot",
    },
  ];

  const [messages, setMessages] = useState(welcomeMessages);

  const [loading, setLoading] = useState(false);

  const [chatId, setChatId] = useState(null);

  // ==========================
  // Logout
  // ==========================
  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("name");

    navigate("/");
  }

  // ==========================
  // New Chat
  // ==========================
  async function newChat() {
    try {
      const response = await API.get("/new-chat");

      setChatId(response.data.chat_id);

      setMessages(welcomeMessages);

    } catch (err) {
      console.log(err);
    }
  }

  // ==========================
  // Load Old Chat
  // ==========================
  async function loadConversation(id) {

    try {

      const response = await API.get(`/history/${id}`);

      const chats = response.data.map((chat) => ({
        text: chat.message,
        sender: chat.sender,
      }));

      setMessages(chats);

      setChatId(id);

    } catch (err) {

      console.log(err);

    }

  }

  // ==========================
  // Send Message
  // ==========================
  async function sendMessage(text) {

    if (text.trim() === "" || loading) return;

    setLoading(true);

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

        chat_id: chatId,

      });

      if (!chatId) {

        setChatId(response.data.chat_id);

      }

      setMessages((prev) => {

        const updated = [...prev];

        updated.pop();

        updated.push({

          text: response.data.reply,

          sender: "bot",

        });

        return updated;

      });

    } catch (error) {

      console.log(error);

      setMessages((prev) => {

        const updated = [...prev];

        updated.pop();

        updated.push({

          text: "❌ Backend Connection Failed.",

          sender: "bot",

        });

        return updated;

      });

    } finally {

      setLoading(false);

    }

  }

  return (

    <div className="app">

      <Header />

      {/* Top Bar */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px 20px",
          background: "#f5f5f5",
          borderBottom: "1px solid #ddd",
        }}
      >

        <h3>
          👋 Welcome, {username}
        </h3>

        <button
          onClick={logout}
          style={{
            padding: "8px 15px",
            background: "#ff4d4f",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>

      </div>

      <div className="main-content">

        <Sidebar
          newChat={newChat}
          loadConversation={loadConversation}
        />

        <div className="chat-section">

          <ChatBox
            messages={messages}
          />

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