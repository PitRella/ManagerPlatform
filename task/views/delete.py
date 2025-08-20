from abc import ABC
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXResponseMixin
from task.models import Task
from task.services import TaskService


class TaskDeleteView(
    LoginRequiredMixin,
    DeleteView # type: ignore
):
    """View for deleting tasks via HTMX."""
    
    model = Task

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.task_service: TaskService = TaskService()

    def delete(self, request, *args, **kwargs):
        """Handle DELETE request."""
        try:
            self.task_service.delete_task(
                task_id=self.get_object().id,
                user=request.user
            )
            return HttpResponse('', status=204)
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    def post(self, request, *args, **kwargs):
        """Handle POST request for deletion."""
        return self.delete(request, *args, **kwargs)
