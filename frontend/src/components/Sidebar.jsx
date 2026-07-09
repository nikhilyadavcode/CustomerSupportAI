function Sidebar() {
  return (
    <aside className="sidebar">
      <button className="new-chat-btn">
        + New Chat
      </button>

      <h3>Chat History</h3>

      <ul>
        <li>Billing Issue</li>
        <li>Refund Request</li>
        <li>Technical Support</li>
      </ul>
    </aside>
  );
}

export default Sidebar;