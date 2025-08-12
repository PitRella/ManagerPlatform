from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json
from django.template.loader import render_to_string
from django.contrib import messages
from django.db import models
from task.models import Task
from task.forms import TaskForm, TaskEditForm
from project.models import Project


class TaskCreateView(CreateView):
    """View for creating new tasks via HTMX."""
    model = Task
    form_class = TaskForm
    template_name = 'task/task_item.html'

    def post(self, request, *args, **kwargs):
        """Handle POST request to create task from text."""
        project_id = self.kwargs.get('project_id')
        task_text = request.POST.get('searchInput-' + str(project_id),
                                     '').strip()
        if not task_text:
            return HttpResponse('Task text cannot be empty.', status=400)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return HttpResponse('Project not found.', status=404)

        max_priority = Task.objects.filter(project=project).aggregate(
            models.Max('priority')
        )['priority__max'] or 0
        next_priority = max_priority + 1

        task = Task.objects.create(
            text=task_text,
            project=project,
            priority=next_priority
        )

        messages.success(
            request,
            f'Task "{task.text}" was created successfully!'
        )

        task_html = render_to_string('task/task_item.html', {
            'task': task
        }, request=request)

        response_html = task_html

        if project_id:
            oob_clear_input = render_to_string('task/oob_clear_input.html', {
                'project_id': project_id
            }, request=request)

            oob_remove_message = render_to_string(
                'task/oob_remove_no_tasks.html', {
                    'project_id': project_id
                }, request=request)

            response_html += oob_clear_input + oob_remove_message

        return HttpResponse(response_html)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskEditForm
    template_name = 'task/task_text_edit.html'

    def form_valid(self, form):
        task = form.save()
        html = render_to_string('task/task_text_display.html', {
            'task': task
        }, request=self.request)
        return HttpResponse(html)

    def form_invalid(self, form):
        html = render_to_string('task/task_text_edit.html', {
            'form': form,
            'task': self.get_object()
        }, request=self.request)
        return HttpResponse(html, status=422)



class TaskDeleteView(DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return HttpResponse('', status=204)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@require_POST
def reorder_tasks(request):
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


def create_task_simple(request, project_id):
    """Simple view for creating tasks without CSRF check."""
    if request.method == 'POST':
        task_text = request.POST.get('searchInput-' + str(project_id),
                                     '').strip()

        if not task_text:
            return HttpResponse('Task text cannot be empty.', status=400)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return HttpResponse('Project not found.', status=404)

        max_priority = Task.objects.filter(project=project).aggregate(
            models.Max('priority')
        )['priority__max'] or 0
        next_priority = max_priority + 1

        task = Task.objects.create(
            text=task_text,
            project=project,
            priority=next_priority
        )

        task_html = render_to_string('task/task_item.html', {
            'task': task
        }, request=request)

        response_html = task_html

        if project_id:
            oob_clear_input = render_to_string('task/oob_clear_input.html', {
                'project_id': project_id
            }, request=request)

            oob_remove_message = render_to_string(
                'task/oob_remove_no_tasks.html', {
                    'project_id': project_id
                }, request=request)

            response_html += oob_clear_input + oob_remove_message

        return HttpResponse(response_html)

    return HttpResponse('Method not allowed', status=405)


@require_POST
def toggle_task(request, pk):
    """Toggle the completed status of a task."""
    try:
        task = Task.objects.get(pk=pk)
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