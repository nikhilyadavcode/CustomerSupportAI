import { useEffect, useState } from "react";
import API from "../services/api";

function Sidebar({ newChat }) {

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

        {history
          .filter((chat) => chat.sender === "user")
          .map((chat, index) => (

            <li key={index}>
              {chat.message.length > 30
                ? chat.message.substring(0, 30) + "..."
                : chat.message}
            </li>

          ))}

      </ul>

    </aside>
  );
}

export default Sidebar;