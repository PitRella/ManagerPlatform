from typing import Optional, Dict, List, TYPE_CHECKING
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class ProjectRepository:
    """Repository for managing Project data access operations."""

    def __init__(self) -> None:
        self.model = Project

    def get_user_projects(
            self,
            user: User,
            limit: Optional[int] = None,
            include_archived: bool = False
    ) -> QuerySet[Project]:
        """Get projects for a specific user."""
        queryset: QuerySet[Project] = self.model.objects.for_user(user)

        if limit:
            queryset = queryset[:limit]

        return queryset

    def get_project_by_id(
            self,
            project_id: int,
            user: User
    ) -> Project:
        """Get a specific project by ID for a user."""
        return self.model.objects.for_user(user).get(id=project_id)

    def create_project(
            self,
            title: str,
            user: User
    ) -> Project:
        """Create a new project."""
        return self.model.objects.create(title=title, owner=user)

    def update_project(
            self,
            project_id: int,
            title: str,
            user: User
    ) -> Project:
        """Update an existing project."""
        project: Project = self.get_project_by_id(project_id, user)
        project.title = title
        project.save()
        return project

    def delete_project(
            self,
            project_id: int,
            user: User
    ) -> bool:
        """Delete a project."""
        project: Project = self.get_project_by_id(project_id, user)
        project.delete()
        return True

    def project_exists(
            self,
            title: str,
            user: User
    ) -> bool:
        """Check if a project with given title exists for a user."""
        return self.model.objects.for_user(user).filter(title=title).exists()

    def get_project_stats(
            self,
            user: User
    ) -> Dict[str, int]:
        """Get project statistics for a user."""
        total_projects: int = self.model.objects.for_user(user).count()
        active_projects: int = total_projects
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'archived_projects': 0
        }

    def search_projects(self, user: User, query: str) -> QuerySet[Project]:
        """Search projects by title for a user."""
        return self.model.objects.for_user(user).filter(title__icontains=query)
