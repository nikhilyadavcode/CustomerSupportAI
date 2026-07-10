import { useEffect, useState } from "react";
import API from "../services/api";

function Sidebar({ newChat, loadConversation }) {

  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const response = await API.get("/history");
      setHistory(response.data);
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <aside className="sidebar">

      <button
        className="new-chat-btn"
        onClick={newChat}
      >
        + New Chat
      </button>

      <h3>Chat History</h3>

      <ul>
        {history.map((chat) => (
          <li
            key={chat.chat_id}
            onClick={() => loadConversation(chat.chat_id)}
            style={{
              cursor: "pointer",
              padding: "8px",
              borderBottom: "1px solid #ddd",
            }}
          >
            {chat.title.length > 30
              ? chat.title.substring(0, 30) + "..."
              : chat.title}
          </li>
        ))}
      </ul>

    </aside>
  );
}

export default Sidebar;