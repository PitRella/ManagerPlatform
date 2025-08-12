from django.views.generic import DeleteView
from django.http import HttpResponse
from task.models import Task


class TaskDeleteView(DeleteView):
    """View for deleting tasks via HTMX."""
    model = Task

    def delete(self, request, *args, **kwargs):
        """Handle DELETE request."""
        task = self.get_object()
        task.delete()
        return HttpResponse('', status=204)

    def post(self, request, *args, **kwargs):
        """Handle POST request for deletion."""
        return self.delete(request, *args, **kwargs)
