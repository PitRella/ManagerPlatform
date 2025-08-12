from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import UpdateView
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXResponseMixin
from project.forms import EditForm
from project.models import Project
from project.services import ProjectService


class ProjectUpdateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Project],
    UpdateView  # type: ignore
):
    """View for updating Project instances.

    Inherits from:
        LoginRequiredMixin: Ensures user authentication
        HTMXResponseMixin: Handles HTMX-specific responses
        UpdateView: Provides base update functionality

    The view handles project updates and returns appropriate HTMX responses
    for updating the project title in the UI.
    """

    model = Project
    form_class = EditForm
    template_name = 'project/edit.html'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.project_service: ProjectService = ProjectService()

    def get_queryset(
            self
    ) -> QuerySet[Project]:
        """Get queryset of projects filtered for the current user.

        Returns:
            QuerySet of Project instances that belong to the current user.

        """
        return Project.objects.for_user(self.request.user)

    def form_valid(self, form: Any) -> HttpResponse:
        """Process valid form submission using service layer."""
        try:
            project: Project = self.project_service.update_project(
                project_id=self.get_object().id,
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
        """Render HTMX response for project title update.

        Args:
            instance: Project instance that was updated.

        Returns:
            HttpResponse containing the rendered project title template.

        """
        html = render_to_string(
            'project/edit_title.html',
            {
                'project':
                    instance
            },
            request=self.request
        )
        return HttpResponse(html)

