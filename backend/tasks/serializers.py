from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Board, Column, Task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'order', 'due_date', 'created_at']


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # inclui as tarefas ao buscar a coluna

    class Meta:
        model = Column
        fields = ['id', 'title', 'order', 'tasks']


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)  # inclui as colunas ao buscar o board
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'columns', 'created_at']


class BoardListSerializer(serializers.ModelSerializer):
    """Versão resumida do board para listagem (sem colunas e tarefas)"""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'created_at']


class MoveTaskSerializer(serializers.Serializer):
    """Usado para mover uma tarefa de coluna"""
    column_id = serializers.IntegerField()
    order = serializers.IntegerField()
