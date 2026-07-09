import { useState } from "react";

function InputBox({ sendMessage }) {

  const [text, setText] = useState("");

  function handleSend() {

    sendMessage(text);

    setText("");

  }

  return (

    <footer className="input-area">

      <input
  type="text"
  placeholder="Type your message..."
  value={text}
  onChange={(e) => setText(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  }}
/>

      <button onClick={handleSend}>
        Send
      </button>

    </footer>

  );
}

export default InputBox;