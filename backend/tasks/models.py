from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """Um board é o quadro kanban principal. Ex: 'Trabalho', 'Estudos'"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.owner.username})"


class Column(models.Model):
    """Uma coluna dentro do board. Ex: 'A fazer', 'Em progresso', 'Concluído'"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)  # controla a ordem das colunas

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} — {self.board.title}"


class Task(models.Model):
    """Uma tarefa dentro de uma coluna."""

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Baixa'),
        (PRIORITY_MEDIUM, 'Média'),
        (PRIORITY_HIGH, 'Alta'),
    ]

    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    order = models.PositiveIntegerField(default=0)  # ordem dentro da coluna
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} [{self.priority}]"
