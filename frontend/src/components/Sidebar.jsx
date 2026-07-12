import { useEffect, useState } from "react";
import { FaPlus, FaHistory, FaUserCircle, FaSignOutAlt } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Sidebar({ newChat, loadConversation }) {

  const [history, setHistory] = useState([]);

  const navigate = useNavigate();

  const username = localStorage.getItem("name") || "User";

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

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("name");
    navigate("/");
  }

  return (
    <aside className="sidebar">

      <div className="profile">

  <FaUserCircle className="profile-icon" />

  <h2>{username}</h2>

  <p>AI Assistant User</p>

  <span className="online-status">
    🟢 Online
  </span>

</div>

      <button
        className="new-chat-btn"
        onClick={newChat}
      >
        <FaPlus /> New Chat
      </button>

      <div className="history-title">

        <FaHistory />

        <span>Chat History</span>

      </div>

      <ul className="history-list">

        {history.map((chat) => (

          <li
            key={chat.chat_id}
            onClick={() => loadConversation(chat.chat_id)}
          >

            {chat.title.length > 28
              ? chat.title.substring(0, 28) + "..."
              : chat.title}

          </li>

        ))}

      </ul>

      <button
        className="logout-btn"
        onClick={logout}
      >
        <FaSignOutAlt />

        Logout
      </button>

    </aside>
  );
}

export default Sidebar;