from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    CreateView,
)

from core.mixins.views import HTMXResponseMixin
from project.forms import CreateForm
from project.models import Project


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
