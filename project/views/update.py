from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import UpdateView

from core.mixins.views import HTMXResponseMixin
from project.forms import EditForm
from project.models import Project


class ProjectUpdateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Project],
    UpdateView
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

    def get_queryset(self):
        """Get queryset of projects filtered for the current user.

        Returns:
            QuerySet of Project instances that belong to the current user.

        """
        return Project.objects.for_user(self.request.user)

    def render_htmx_response(self, instance: Project) -> HttpResponse:
        """Render HTMX response for project title update.

        Args:
            instance: Project instance that was updated.

        Returns:
            HttpResponse containing rendered project title template.

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
