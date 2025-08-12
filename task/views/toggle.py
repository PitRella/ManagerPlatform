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
class TaskToggleView(
    LoginRequiredMixin,
    HTMXResponseMixin[Task],
    View
):
    """View for toggling task completion status."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.task_service: TaskService = TaskService()

    def post(self, request, *args, **kwargs):
        """Handle POST request to toggle task completion."""
        try:
            payload = json.loads(request.body.decode('utf-8'))
            completed = payload.get('completed', False)
            task_id = self.kwargs.get('pk')

            task: Task = self.task_service.toggle_task_completion(
                task_id=task_id,
                user=request.user,
                completed=completed
            )

            return JsonResponse({
                'status': 'success',
                'completed': task.completed
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
