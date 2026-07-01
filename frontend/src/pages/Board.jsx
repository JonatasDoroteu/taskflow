import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  DndContext,
  closestCorners,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { useDroppable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import api from "../api/api";

function Board() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [columns, setColumns] = useState([]);
  const [novaColuna, setNovaColuna] = useState("");
  const [erro, setErro] = useState("");

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: { distance: 5 },
    })
  );

  useEffect(() => {
    carregarColunas();
  }, []);

  async function carregarColunas() {
    try {
      const response = await api.get(`/boards/${id}/columns/`);
      const colunasComTarefas = await Promise.all(
        response.data.map(async (coluna) => {
          const tarefasResp = await api.get(`/columns/${coluna.id}/tasks/`);
          return { ...coluna, tasks: tarefasResp.data };
        })
      );
      setColumns(colunasComTarefas);
    } catch (err) {
      setErro("Erro ao carregar colunas");
    }
  }

  async function criarColuna(e) {
    e.preventDefault();
    if (!novaColuna.trim()) return;

    try {
      await api.post(`/boards/${id}/columns/`, {
        title: novaColuna,
        order: columns.length,
      });
      setNovaColuna("");
      carregarColunas();
    } catch (err) {
      setErro("Erro ao criar coluna");
    }
  }

  async function editarColuna(columnId, novoTitulo) {
    if (!novoTitulo.trim()) return;

    try {
      await api.patch(`/columns/${columnId}/`, { title: novoTitulo });
      carregarColunas();
    } catch (err) {
      setErro("Erro ao editar coluna");
    }
  }

  async function excluirColuna(columnId) {
    if (
      !window.confirm(
        "Excluir esta coluna também excluirá todas as tarefas dentro dela. Continuar?"
      )
    )
      return;

    try {
      await api.delete(`/columns/${columnId}/`);
      carregarColunas();
    } catch (err) {
      setErro("Erro ao excluir coluna");
    }
  }

  async function criarTarefa(columnId, titulo, prioridade) {
    if (!titulo.trim()) return;

    try {
      await api.post(`/columns/${columnId}/tasks/`, {
        title: titulo,
        priority: prioridade,
        order: 0,
      });
      carregarColunas();
    } catch (err) {
      setErro("Erro ao criar tarefa");
    }
  }

  async function editarTarefa(taskId, dados) {
    try {
      await api.patch(`/tasks/${taskId}/`, dados);
      carregarColunas();
    } catch (err) {
      setErro("Erro ao editar tarefa");
    }
  }

  async function excluirTarefa(taskId) {
    if (!window.confirm("Tem certeza que deseja excluir esta tarefa?")) return;

    try {
      await api.delete(`/tasks/${taskId}/`);
      carregarColunas();
    } catch (err) {
      setErro("Erro ao excluir tarefa");
    }
  }

  function encontrarColunaDaTarefa(taskId, cols) {
    return cols.find((c) => (c.tasks || []).some((t) => t.id === taskId));
  }

  async function handleDragEnd(event) {
    const { active, over } = event;
    if (!over) return;

    const activeId = active.id; // id da task arrastada
    const overId = over.id; // id da task OU da coluna onde soltou

    setColumns((prev) => {
      const cols = prev.map((c) => ({ ...c, tasks: [...(c.tasks || [])] }));

      const origemCol = encontrarColunaDaTarefa(activeId, cols);
      if (!origemCol) return prev;

      // Coluna de destino: se soltou em cima de uma task, pega a coluna dela;
      // se soltou direto na coluna (área vazia), overId já é o id da coluna
      let destinoCol = encontrarColunaDaTarefa(overId, cols);
      if (!destinoCol) {
        destinoCol = cols.find((c) => c.id === overId);
      }
      if (!destinoCol) return prev;

      const taskArrastada = origemCol.tasks.find((t) => t.id === activeId);
      if (!taskArrastada) return prev;

      // Remove da coluna de origem
      origemCol.tasks = origemCol.tasks.filter((t) => t.id !== activeId);

      // Calcula posição de inserção na coluna de destino
      let novoIndex = destinoCol.tasks.findIndex((t) => t.id === overId);
      if (novoIndex === -1) novoIndex = destinoCol.tasks.length;

      destinoCol.tasks.splice(novoIndex, 0, taskArrastada);

      // Reordena localmente (order = índice na coluna)
      destinoCol.tasks = destinoCol.tasks.map((t, idx) => ({ ...t, order: idx }));

      // Persiste no backend
      api
        .patch(`/tasks/${activeId}/move/`, {
          column_id: destinoCol.id,
          order: novoIndex,
        })
        .catch(() => setErro("Erro ao mover tarefa"));

      return cols;
    });
  }

  return (
    <div className="board-page">
      <div className="board-topbar">
        <button className="back-btn" onClick={() => navigate("/boards")}>
          ← Voltar
        </button>
      </div>

      <form className="new-column-form" onSubmit={criarColuna}>
        <input
          type="text"
          placeholder="Nome da nova coluna"
          value={novaColuna}
          onChange={(e) => setNovaColuna(e.target.value)}
        />
        <button type="submit">Adicionar coluna</button>
      </form>

      {erro && <p className="error-banner">{erro}</p>}

      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragEnd={handleDragEnd}
      >
        <div className="board-lanes">
          {columns.map((coluna) => (
            <ColunaCard
              key={coluna.id}
              coluna={coluna}
              onCriarTarefa={criarTarefa}
              onEditarTarefa={editarTarefa}
              onExcluirTarefa={excluirTarefa}
              onEditarColuna={editarColuna}
              onExcluirColuna={excluirColuna}
            />
          ))}
        </div>
      </DndContext>
    </div>
  );
}

function ColunaCard({
  coluna,
  onCriarTarefa,
  onEditarTarefa,
  onExcluirTarefa,
  onEditarColuna,
  onExcluirColuna,
}) {
  const [novaTarefa, setNovaTarefa] = useState("");
  const [novaPrioridade, setNovaPrioridade] = useState("medium");
  const [editandoColuna, setEditandoColuna] = useState(false);
  const [tituloColuna, setTituloColuna] = useState(coluna.title);

  const { setNodeRef } = useDroppable({ id: coluna.id });

  function handleSubmit(e) {
    e.preventDefault();
    onCriarTarefa(coluna.id, novaTarefa, novaPrioridade);
    setNovaTarefa("");
    setNovaPrioridade("medium");
  }

  function salvarColuna() {
    if (!tituloColuna.trim()) return;
    onEditarColuna(coluna.id, tituloColuna);
    setEditandoColuna(false);
  }

  function cancelarEdicaoColuna() {
    setTituloColuna(coluna.title);
    setEditandoColuna(false);
  }

  const tasks = coluna.tasks || [];
  const taskIds = tasks.map((t) => t.id);

  return (
    <div className="column-card">
      <div className="column-header">
        {editandoColuna ? (
          <input
            type="text"
            className="column-title-input"
            value={tituloColuna}
            onChange={(e) => setTituloColuna(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && salvarColuna()}
            autoFocus
          />
        ) : (
          <h3 className="column-title">{coluna.title}</h3>
        )}
        <span className="column-count">{tasks.length}</span>
      </div>

      <div className="column-actions">
        {editandoColuna ? (
          <>
            <button className="column-action-btn" onClick={salvarColuna}>
              Salvar
            </button>
            <button
              className="column-action-btn column-action-cancel"
              onClick={cancelarEdicaoColuna}
            >
              Cancelar
            </button>
          </>
        ) : (
          <>
            <button
              className="column-action-btn"
              onClick={() => setEditandoColuna(true)}
            >
              Renomear
            </button>
            <button
              className="column-action-btn column-action-delete"
              onClick={() => onExcluirColuna(coluna.id)}
            >
              Excluir
            </button>
          </>
        )}
      </div>

      <SortableContext items={taskIds} strategy={verticalListSortingStrategy}>
        <div className="task-list" ref={setNodeRef}>
          {tasks.length === 0 && (
            <div className="column-empty">Sem tarefas ainda</div>
          )}

          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onEditar={onEditarTarefa}
              onExcluir={onExcluirTarefa}
            />
          ))}
        </div>
      </SortableContext>

      <form className="new-task-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nova tarefa"
          value={novaTarefa}
          onChange={(e) => setNovaTarefa(e.target.value)}
        />
        <select
          className="priority-select"
          value={novaPrioridade}
          onChange={(e) => setNovaPrioridade(e.target.value)}
        >
          <option value="low">Baixa</option>
          <option value="medium">Média</option>
          <option value="high">Alta</option>
        </select>
      </form>
    </div>
  );
}

function TaskCard({ task, onEditar, onExcluir }) {
  const [editando, setEditando] = useState(false);
  const [titulo, setTitulo] = useState(task.title);
  const [prioridade, setPrioridade] = useState(task.priority);

  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
  };

  function salvar() {
    if (!titulo.trim()) return;
    onEditar(task.id, { title: titulo, priority: prioridade });
    setEditando(false);
  }

  function cancelar() {
    setTitulo(task.title);
    setPrioridade(task.priority);
    setEditando(false);
  }

  if (editando) {
    return (
      <div className="task-card task-card-editing" ref={setNodeRef} style={style}>
        <input
          type="text"
          className="task-edit-input"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          autoFocus
        />
        <select
          className="priority-select"
          value={prioridade}
          onChange={(e) => setPrioridade(e.target.value)}
        >
          <option value="low">Baixa</option>
          <option value="medium">Média</option>
          <option value="high">Alta</option>
        </select>
        <div className="task-edit-actions">
          <button className="task-save-btn" onClick={salvar}>Salvar</button>
          <button className="task-cancel-btn" onClick={cancelar}>Cancelar</button>
        </div>
      </div>
    );
  }

  return (
    <div
      className="task-card"
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
    >
      <span className="task-title">{task.title}</span>
      <div className="task-meta">
        <span className={`priority-tag ${task.priority}`}>
          {task.priority === "high"
            ? "alta"
            : task.priority === "low"
            ? "baixa"
            : "média"}
        </span>
        <div className="task-actions">
          <button
            className="task-icon-btn"
            onClick={(e) => {
              e.stopPropagation();
              setEditando(true);
            }}
            onPointerDown={(e) => e.stopPropagation()}
            title="Editar"
          >
            ✎
          </button>
          <button
            className="task-icon-btn task-icon-delete"
            onClick={(e) => {
              e.stopPropagation();
              onExcluir(task.id);
            }}
            onPointerDown={(e) => e.stopPropagation()}
            title="Excluir"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
}

export default Board;