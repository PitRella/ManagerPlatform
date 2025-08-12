from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    CreateView,
)

from core.mixins.views import HTMXResponseMixin
from project.forms import CreateForm
from project.models import Project


class ProjectCreateView(LoginRequiredMixin, HTMXResponseMixin[Project],
                        CreateView):
    """View for creating new projects via HTMX."""

    model = Project
    form_class = CreateForm
    template_name = 'project/create.html'
    success_template = 'project/project_item.html'

    def form_valid(
            self,
            form: CreateForm
    ) -> HttpResponse:
        """Process valid form submission.

        Sets the project owner to the current user and saves the form.

        Args:
            form: Validated CreateForm instance containing project data

        Returns:
            HttpResponse with rendered success template

        """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def render_htmx_response(
            self,
            instance: Project
    ) -> HttpResponse:
        """Render HTMX response for successful project creation.

        Args:
            instance: Project instance that was created.

        Returns:
            HttpResponse containing rendered project template.

        """
        html = render_to_string(
            self.success_template,
            {'project': instance},
            request=self.request
        )
        return HttpResponse(html)
