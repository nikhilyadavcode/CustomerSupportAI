import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api";

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    try {
      await API.post("/auth/register", {
        name,
        email,
        password,
      });

      alert("Registration Successful");

      navigate("/");
    } catch (err) {
      alert("Registration Failed");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Register</h1>

      <input
        placeholder="Name"
        onChange={(e) => setName(e.target.value)}
      />

      <br />
      <br />

      <input
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

      <button onClick={register}>Register</button>

      <br />
      <br />

      <Link to="/">Already have an account?</Link>
    </div>
  );
}

export default Register;