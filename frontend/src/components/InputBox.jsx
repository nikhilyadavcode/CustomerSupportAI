import { useState } from "react";
import { FaPaperPlane } from "react-icons/fa";

function InputBox({ sendMessage, loading }) {

  const [text, setText] = useState("");

  function handleSend() {

    if (text.trim() === "" || loading) return;

    sendMessage(text);

    setText("");

  }

  return (

    <footer className="input-area">

      <input

        type="text"

        placeholder={
          loading
            ? "🤖 AI is typing..."
            : "Ask anything about orders, products, refund..."
        }

        value={text}

        disabled={loading}

        onChange={(e) => setText(e.target.value)}

        onKeyDown={(e) => {

          if (e.key === "Enter") {

            handleSend();

          }

        }}

      />

      <button

        onClick={handleSend}

        disabled={loading}

      >

        {loading ? "Sending..." : <FaPaperPlane />}

      </button>

    </footer>

  );

}

export default InputBox;