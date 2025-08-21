from typing import Any, Dict, cast
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.core.exceptions import ValidationError
from django.contrib import messages

from core.mixins.views import HTMXResponseMixin
from task.forms import TaskForm
from task.models import Task
from task.services import TaskService


class TaskCreateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Task],
    CreateView  # type: ignore
):
    """View for creating new tasks via HTMX."""

    model = Task
    form_class = TaskForm
    template_name = 'task/task_item.html'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.task_service: TaskService = TaskService()

    def post(self, request, *args, **kwargs):
        """Handle POST request to create task from text."""
        project_id = self.kwargs.get('project_id')
        task_text = request.POST.get(f'searchInput-{project_id}', '').strip()

        if not task_text:
            return HttpResponse('Task text cannot be empty.', status=400)

        try:
            task: Task = self.task_service.create_task(
                text=task_text,
                project_id=project_id,
                user=request.user
            )

            messages.success(
                request,
                f'Task "{task.text}" was created successfully!'
            )

            return self.render_htmx_response(task)

        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    def render_htmx_response(
            self,
            instance: models.Model
    ) -> HttpResponse:
        """Render HTMX response for successful task creation."""
        task = cast(Task, instance)
        
        task_html = render_to_string('task/task_item.html', {
            'task': task
        }, request=self.request)

        return HttpResponse(task_html)
