from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
import json
from task.models import Task


@method_decorator(require_POST, name='dispatch')
class TaskToggleView(View):
    """View for toggling task completion status."""
    
    def post(self, request, *args, **kwargs):
        """Handle POST request to toggle task completion."""
        try:
            task = Task.objects.get(pk=self.kwargs.get('pk'))
            payload = json.loads(request.body.decode('utf-8'))
            completed = payload.get('completed', False)

            task.completed = completed
            task.save(update_fields=['completed'])

            return JsonResponse({
                'status': 'success',
                'completed': task.completed
            })
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
