from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from core.mixins.views import HTMXDeleteMixin
from project.models import Project
from project.services import ProjectService


class ProjectDeleteView(
    LoginRequiredMixin,
    HTMXDeleteMixin,
    DeleteView  # type: ignore
):
    """View for deleting Project instances.

    Inherits from:
        LoginRequiredMixin: Ensures user authentication
        HTMXDeleteMixin: Handles HTMX-specific delete responses
        DeleteView: Provides base deletion functionality

    The view handles project deletion and ensures only authenticated users
    can delete projects. It integrates with HTMX for smooth UI updates
    after deletion.
    """

    model = Project
    template_name = 'project/delete.html'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.project_service: ProjectService = ProjectService()

    def post(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST request for HTMX-based deletion using service layer."""
        try:
            self.project_service.delete_project(
                project_id=self.get_object().id,
                user=request.user
            )
            return HttpResponse('', status=204)
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

