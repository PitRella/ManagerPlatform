import json
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXResponseMixin
from task.models import Task
from task.services import TaskService


@method_decorator(require_POST, name='dispatch')
class TaskReorderView(
    LoginRequiredMixin,
    View
):
    """View for reordering tasks via drag and drop."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.task_service: TaskService = TaskService()

    def post(self, request, *args, **kwargs):
        """Handle POST request to reorder tasks."""
        try:
            payload = json.loads(request.body.decode('utf-8'))
            order = payload.get('order', [])

            self.task_service.reorder_tasks(
                order_data=order,
                user=request.user
            )

            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
