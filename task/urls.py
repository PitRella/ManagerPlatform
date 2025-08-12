from django.urls import path
from task.views import TaskCreateView, TaskUpdateView, TaskDeleteView, reorder_tasks, create_task_simple, toggle_task

app_name = 'tasks'

urlpatterns = [
    path('<int:project_id>/create/', TaskCreateView.as_view(), name='create'),
    path('<int:project_id>/create-simple/', create_task_simple, name='create_simple'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle/', toggle_task, name='toggle'),
    path('reorder/', reorder_tasks, name='reorder'),
]
