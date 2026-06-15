from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Boards
    path('boards/', views.BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', views.BoardDetailView.as_view(), name='board-detail'),

    # Columns
    path('boards/<int:board_id>/columns/', views.ColumnListCreateView.as_view(), name='column-list'),
    path('columns/<int:pk>/', views.ColumnDetailView.as_view(), name='column-detail'),

    # Tasks
    path('columns/<int:column_id>/tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/move/', views.move_task, name='task-move'),
]
