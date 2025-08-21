from django.urls import path
from task.views.create import TaskCreateView
from task.views.update import TaskUpdateView
from task.views.delete import TaskDeleteView
from task.views.reorder import TaskReorderView
from task.views.toggle import TaskToggleView

app_name = 'tasks'

urlpatterns = [
    path('<int:project_id>/create/', TaskCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle/', TaskToggleView.as_view(), name='toggle'),
    path('reorder/', TaskReorderView.as_view(), name='reorder'),
]
