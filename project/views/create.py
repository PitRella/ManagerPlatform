from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    CreateView,
)
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXResponseMixin
from project.forms import CreateForm
from project.models import Project
from project.services import ProjectService


class ProjectCreateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Project],
    CreateView  # type: ignore
):
    """View for creating new projects via HTMX."""

    model = Project
    form_class = CreateForm
    template_name = 'project/create.html'
    success_template = 'project/project_item.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_service = ProjectService()

    def form_valid(
            self,
            form: CreateForm  # type: ignore
    ) -> HttpResponse:
        """Process valid form submission using service layer.

        Args:
            form: Validated CreateForm instance containing project data

        Returns:
            HttpResponse with rendered success template

        """
        try:
            project = self.project_service.create_project(
                title=form.cleaned_data['title'],
                user=self.request.user
            )
            return self.render_htmx_response(project)
        except ValidationError as e:
            form.add_error('title', e)
            return self.form_invalid(form)

    def render_htmx_response(
            self,
            instance: Project  # type: ignore
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

