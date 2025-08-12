from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
import json
from task.models import Task


@method_decorator(require_POST, name='dispatch')
class TaskReorderView(View):
    """View for reordering tasks via drag and drop."""
    
    def post(self, request, *args, **kwargs):
        """Handle POST request to reorder tasks."""
        try:
            payload = json.loads(request.body.decode('utf-8'))
            order = payload.get('order', [])
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        for item in order:
            try:
                task = Task.objects.get(pk=item['id'])
                task.priority = int(item['position'])
                task.save(update_fields=['priority'])
            except Exception:
                continue

        return JsonResponse({'status': 'ok'})
