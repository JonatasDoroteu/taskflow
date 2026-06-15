from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Board, Column, Task
from .serializers import (
    RegisterSerializer,
    BoardSerializer,
    BoardListSerializer,
    ColumnSerializer,
    TaskSerializer,
    MoveTaskSerializer,
)


# ── Autenticação ────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """POST /api/register/ — cria novo usuário"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ── Boards ──────────────────────────────────────────────────────────────────

class BoardListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/boards/ — lista os boards do usuário logado
    POST /api/boards/ — cria um novo board
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardListSerializer
        return BoardListSerializer

    def get_queryset(self):
        # Usuário só vê os próprios boards
        return Board.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/boards/{id}/ — detalhes do board com colunas e tarefas
    PUT    /api/boards/{id}/ — edita o board
    DELETE /api/boards/{id}/ — deleta o board
    """
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


# ── Columns ─────────────────────────────────────────────────────────────────

class ColumnListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/boards/{board_id}/columns/ — lista colunas do board
    POST /api/boards/{board_id}/columns/ — cria uma coluna
    """
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board = get_object_or_404(Board, id=self.kwargs['board_id'], owner=self.request.user)
        return Column.objects.filter(board=board)

    def perform_create(self, serializer):
        board = get_object_or_404(Board, id=self.kwargs['board_id'], owner=self.request.user)
        serializer.save(board=board)


class ColumnDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT    /api/columns/{id}/ — edita a coluna
    DELETE /api/columns/{id}/ — deleta a coluna
    """
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)


# ── Tasks ────────────────────────────────────────────────────────────────────

class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/columns/{column_id}/tasks/ — lista tarefas da coluna
    POST /api/columns/{column_id}/tasks/ — cria uma tarefa
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        column = get_object_or_404(
            Column,
            id=self.kwargs['column_id'],
            board__owner=self.request.user
        )
        return Task.objects.filter(column=column)

    def perform_create(self, serializer):
        column = get_object_or_404(
            Column,
            id=self.kwargs['column_id'],
            board__owner=self.request.user
        )
        serializer.save(column=column)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tasks/{id}/ — detalhes da tarefa
    PUT    /api/tasks/{id}/ — edita a tarefa
    DELETE /api/tasks/{id}/ — deleta a tarefa
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def move_task(request, task_id):
    """
    PATCH /api/tasks/{id}/move/
    Move uma tarefa para outra coluna e/ou muda a ordem.
    Body: { "column_id": 3, "order": 1 }
    """
    task = get_object_or_404(Task, id=task_id, column__board__owner=request.user)
    serializer = MoveTaskSerializer(data=request.data)

    if serializer.is_valid():
        new_column = get_object_or_404(
            Column,
            id=serializer.validated_data['column_id'],
            board__owner=request.user
        )
        task.column = new_column
        task.order = serializer.validated_data['order']
        task.save()
        return Response(TaskSerializer(task).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
