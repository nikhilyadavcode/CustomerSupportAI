import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";

import API from "../services/api";

function Home() {

  const navigate = useNavigate();



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
        text: "🤖AI is Typing...",
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

      
    <div className="welcome-card">

  <div>

    <h2>👋 Welcome, {localStorage.getItem("name")}</h2>

    <p>
      Ask anything about your orders, products, refunds,
      delivery or support tickets.
    </p>

  </div>

  <div className="robot-icon">

    🤖

  </div>

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