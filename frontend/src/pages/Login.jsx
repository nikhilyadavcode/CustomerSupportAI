import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await API.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("name", res.data.name);

      alert("Login Successful");

      navigate("/chat");
    } catch (err) {
      alert("Invalid Email or Password");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Login</h1>

      <input
        type="email"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <br />
      <br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />
      <br />

      <button onClick={login}>Login</button>

      <br />
      <br />

      <Link to="/register">Create Account</Link>
    </div>
  );
}

export default Login;