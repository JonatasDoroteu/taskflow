import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    setErro("");

    try {
      const response = await api.post("/token/", { username, password });
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      navigate("/boards");
    } catch (err) {
      setErro("Usuario ou senha invalidos");
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          <h1>TaskFlow</h1>
          <p>Gerencie suas tarefas com eficiência</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="login-field">
            <label>Usuário</label>
            <input
              type="text"
              placeholder="seu usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="login-field">
            <label>Senha</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="login-btn" type="submit">Entrar</button>

          {erro && <p className="login-error">{erro}</p>}
        </form>
      </div>
    </div>
  );
}

export default Login;