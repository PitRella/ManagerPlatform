from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, \
    View
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from project.models import Project
from project.forms import ProjectForm


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """View for creating new projects via HTMX."""
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        project = form.save()
        # Return the new project HTML to be inserted
        html = render_to_string(
            'project/project_item.html',
            {
                'project': project
            },
            request=self.request)
        return HttpResponse(html)

    def form_invalid(self, form):
        # Return form with errors
        html = render_to_string(
            'project/create.html',
            {
                'form': form
            },
            request=self.request)
        return HttpResponse(html, status=422)
