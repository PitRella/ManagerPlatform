from django.views.generic import UpdateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from task.models import Task
from task.forms import TaskEditForm


class TaskUpdateView(UpdateView):
    """View for updating task text via HTMX."""
    model = Task
    form_class = TaskEditForm
    template_name = 'task/task_text_edit.html'

    def form_valid(self, form):
        """Handle valid form submission."""
        task = form.save()
        html = render_to_string('task/task_text_display.html', {
            'task': task
        }, request=self.request)
        return HttpResponse(html)

    def form_invalid(self, form):
        """Handle invalid form submission."""
        html = render_to_string('task/task_text_edit.html', {
            'form': form,
            'task': self.get_object()
        }, request=self.request)
        return HttpResponse(html, status=422)
