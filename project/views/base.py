"""Base view classes for the project app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from project.services import ProjectService


class ProjectBaseView(LoginRequiredMixin):
    """Base view class for project views with common functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_service = ProjectService()
    
    def get_context_data(self, **kwargs):
        """Add common context data for project views."""
        context = super().get_context_data(**kwargs)
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            context['project_stats'] = self.project_service.get_project_stats(self.request.user)
        return context
