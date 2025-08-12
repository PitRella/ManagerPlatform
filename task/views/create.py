from typing import Any, Dict
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
    CreateView
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

            return self._render_htmx_response(task, project_id)

        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    def _render_htmx_response(self, task: Task, project_id: int) -> HttpResponse:
        """Render HTMX response for successful task creation."""
        task_html = render_to_string('task/task_item.html', {
            'task': task
        }, request=self.request)

        response_html = task_html

        if project_id:
            oob_clear_input = render_to_string('task/oob_clear_input.html', {
                'project_id': project_id
            }, request=self.request)

            oob_remove_message = render_to_string(
                'task/oob_remove_no_tasks.html', {
                    'project_id': project_id
                }, request=self.request)

            response_html += oob_clear_input + oob_remove_message

        return HttpResponse(response_html)


class TaskCreateSimpleView(
    LoginRequiredMixin,
    HTMXResponseMixin[Task],
    CreateView
):
    """Simple view for creating tasks without CSRF check."""
    
    model = Task
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

            return self._render_htmx_response(task, project_id)

        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    def _render_htmx_response(self, task: Task, project_id: int) -> HttpResponse:
        """Render HTMX response for successful task creation."""
        task_html = render_to_string('task/task_item.html', {
            'task': task
        }, request=self.request)

        response_html = task_html

        if project_id:
            oob_clear_input = render_to_string('task/oob_clear_input.html', {
                'project_id': project_id
            }, request=self.request)

            oob_remove_message = render_to_string(
                'task/oob_remove_no_tasks.html', {
                    'project_id': project_id
                }, request=self.request)

            response_html += oob_clear_input + oob_remove_message

        return HttpResponse(response_html)
