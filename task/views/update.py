from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXResponseMixin
from task.models import Task
from task.forms import TaskEditForm
from task.services import TaskService


class TaskUpdateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Task],
    UpdateView
):
    """View for updating task text via HTMX."""
    
    model = Task
    form_class = TaskEditForm
    template_name = 'task/task_text_edit.html'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.task_service: TaskService = TaskService()

    def form_valid(self, form):
        """Handle valid form submission."""
        try:
            task: Task = self.task_service.update_task(
                task_id=self.get_object().id,
                user=self.request.user,
                text=form.cleaned_data['text']
            )
            
            return self.render_htmx_response(task)
            
        except ValidationError as e:
            form.add_error('text', e)
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submission."""
        html = render_to_string('task/task_text_edit.html', {
            'form': form,
            'task': self.get_object()
        }, request=self.request)
        return HttpResponse(html, status=422)

    def render_htmx_response(
            self,
            instance: Task
    ) -> HttpResponse:
        """Render HTMX response for task text update.

        Args:
            instance: Task instance that was updated.

        Returns:
            HttpResponse containing the rendered task text template.

        """
        html = render_to_string(
            'task/task_text_display.html',
            {
                'task': instance
            },
            request=self.request
        )
        return HttpResponse(html)
