from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.template.loader import render_to_string

from core.mixins.views import HTMXResponseMixin
from project.models import Project
from project.forms import EditForm


class ProjectUpdateView(LoginRequiredMixin, HTMXResponseMixin, UpdateView):
    """View for updating project titles via HTMX."""
    model = Project
    form_class = EditForm
    template_name = 'project/edit.html'

    def get_queryset(self):
        """Only projects for current user."""
        return Project.objects.for_user(self.request.user)

    def render_htmx_response(self, instance: Project) -> HttpResponse:
        html = (
            f'<h4 class="mb-0 project-title" '
            f'hx-target="this" hx-swap="outerHTML" '
            f'style="cursor: pointer;" '
            f'title="Click to edit title">{instance.title}</h4>'
        )
        return HttpResponse(html)