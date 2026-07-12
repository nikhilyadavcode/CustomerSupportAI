import { FaRobot, FaUserCircle } from "react-icons/fa";

function Message({ text, sender }) {

  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className={`message-row ${sender}`}>

      <div className="avatar">

        {sender === "bot" ? (
          <FaRobot />
        ) : (
          <FaUserCircle />
        )}

      </div>

      <div className={`message ${sender}`}>

        <div className="message-text">
          {text}
        </div>

        <div className="message-time">
          {time}
        </div>

      </div>

    </div>
  );
}

export default Message;