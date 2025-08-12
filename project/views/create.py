from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, \
    View
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string

from core.mixins.views import HTMXResponseMixin
from project.models import Project
from project.forms import CreateForm


class ProjectCreateView(LoginRequiredMixin, HTMXResponseMixin[Project], CreateView):
    """View for creating new projects via HTMX."""
    model = Project
    form_class = CreateForm
    template_name = 'project/create.html'
    success_template = 'project/project_item.html'

    def form_valid(self, form: CreateForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def render_htmx_response(self, instance: Project) -> HttpResponse:
        html = render_to_string(
            self.success_template,
            {'project': instance},
            request=self.request
        )
        return HttpResponse(html)
