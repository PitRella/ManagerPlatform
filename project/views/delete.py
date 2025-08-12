from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

from core.mixins.views import HTMXDeleteMixin
from project.models import Project


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
