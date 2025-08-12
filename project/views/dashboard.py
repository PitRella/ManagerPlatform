from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView

from project.models import Project


class DashboardView(LoginRequiredMixin, ListView):
    """
    View for displaying a paginated list of projects on the dashboard.

    Inherits from:
        LoginRequiredMixin: Ensures that only authenticated users can access
        ListView: Provides pagination and list display functionality

    Attributes:
        model: Project model used for queryset
        template_name: Template used for rendering the view
        context_object_name: Name used for the project list in template context
        paginate_by: Number of projects displayed per page

    """

    model = Project
    template_name = 'project/dashboard.html'
    context_object_name = 'projects'

    paginate_by = 10

    def get_queryset(self) -> QuerySet[Project]:
        """Returns projects for the current user."""
        return Project.objects.for_user(
            self.request.user
        )
