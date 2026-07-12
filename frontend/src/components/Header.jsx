import { FaRobot } from "react-icons/fa";

function Header() {
  return (
    <header className="header">

      <div className="logo">

        <div className="logo-icon">
          <FaRobot />
        </div>

        <div>

          <h1>AI Customer Support Assistant</h1>

          <p>Your Smart AI Support Partner</p>

          <p className="header-subtitle">
            AI Powered • Gemini AI • Secure Login • Smart Support
          </p>

        </div>

      </div>

    </header>
  );
}

export default Header;