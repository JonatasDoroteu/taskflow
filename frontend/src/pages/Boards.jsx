import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Boards() {
  const [boards, setBoards] = useState([]);
  const [novoNome, setNovoNome] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    carregarBoards();
  }, []);

  async function carregarBoards() {
    try {
      const response = await api.get("/boards/");
      setBoards(response.data);
    } catch (err) {
      setErro("Erro ao carregar boards");
    }
  }

async function criarBoard(e) {
  e.preventDefault();
  if (!novoNome.trim()) return;

  try {
    await api.post("/boards/", { title: novoNome });
    setNovoNome("");
    carregarBoards();
  } catch (err) {
    setErro("Erro ao criar board");
  }
}
  function abrirBoard(id) {
    navigate(`/boards/${id}`);
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  }

 return (
  <div className="boards-page">
    <div className="boards-topbar">
      <div className="boards-brand">
        <h2>TaskFlow</h2>
        <span>/ meus boards</span>
      </div>

      <button className="logout-btn" onClick={logout}>
        Sair
      </button>
    </div>

    {/* resto do componente */}



      <form className="new-board-form" onSubmit={criarBoard}>
        <input
          type="text"
          placeholder="Nome do novo board"
          value={novoNome}
          onChange={(e) => setNovoNome(e.target.value)}
        />
        <button type="submit">Criar</button>
      </form>

      {erro && <p className="error-banner">{erro}</p>}

      {boards.length === 0 ? (
        <div className="boards-empty">Nenhum board criado ainda</div>
      ) : (
        <ul className="boards-list">
          {boards.map((board) => (
            <li
              key={board.id}
              className="board-item"
              onClick={() => abrirBoard(board.id)}
            >
              {board.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Boards;