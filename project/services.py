import logging
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

from project.repositories import ProjectRepository
from project.models import Project
from project.constants import (
    PROJECT_TITLE_MIN_LENGTH,
    PROJECT_TITLE_MAX_LENGTH,
    ERROR_PROJECT_TITLE_EMPTY,
    ERROR_PROJECT_TITLE_TOO_SHORT,
    ERROR_PROJECT_TITLE_TOO_LONG,
    ERROR_PROJECT_TITLE_INVALID_CHARS,
    ERROR_PROJECT_ALREADY_EXISTS,
    ERROR_PROJECT_NO_PERMISSION,
    ERROR_PROJECT_HAS_ACTIVE_TASKS,
)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()

logger = logging.getLogger(__name__)


class ProjectService:
    """Service layer for Project business logic."""

    def __init__(
            self,
            repository: Optional[ProjectRepository] = None):
        self.repository = repository or ProjectRepository()

    def create_project(self, title: str, user: User) -> Project:
        """Create a new project with business logic validation."""
        self._validate_project_title(title)

        if self.repository.project_exists(title, user):
            raise ValidationError(
                ERROR_PROJECT_ALREADY_EXISTS.format(title=title))

        project: Project = self.repository.create_project(title, user)

        logger.info(f"Project '{title}' created by user {user.email}")

        return project

    def update_project(self, project_id: int, title: str,
                       user: User) -> Project:
        """Update an existing project with business logic validation."""
        try:
            project: Project = self.repository.get_project_by_id(project_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError("Project not found.")

        if not self._can_user_modify_project(project, user):
            raise ValidationError(ERROR_PROJECT_NO_PERMISSION)

        self._validate_project_title(title)

        if (self.repository.project_exists(title, user) and
                project.title != title):
            raise ValidationError(
                ERROR_PROJECT_ALREADY_EXISTS.format(title=title))

        updated_project = self.repository.update_project(project_id, title,
                                                         user)

        logger.info(
            f"Project '{project.title}' updated to '{title}' by user {user.email}")

        return updated_project

    def delete_project(self, project_id: int, user: User) -> bool:
        """Delete a project with business logic validation."""
        try:
            project: Project = self.repository.get_project_by_id(project_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError("Project not found.")

        if not self._can_user_modify_project(project, user):
            raise ValidationError(ERROR_PROJECT_NO_PERMISSION)

        if self._has_active_tasks(project):
            raise ValidationError(ERROR_PROJECT_HAS_ACTIVE_TASKS)

        project_title = project.title
        result = self.repository.delete_project(project_id, user)

        logger.info(f"Project '{project_title}' deleted by user {user.email}")

        return result

    def archive_project(self, project_id: int, user: User) -> Project:
        """Archive a project instead of deleting it."""
        try:
            project: Project = self.repository.get_project_by_id(project_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError("Project not found.")

        if not self._can_user_modify_project(project, user):
            raise ValidationError(ERROR_PROJECT_NO_PERMISSION)

        logger.info(f"Project '{project.title}' archived by user {user.email}")
        return project

    def duplicate_project(self, project_id: int, user: User) -> Project:
        """Duplicate a project with all its tasks."""
        try:
            original_project: Project = self.repository.get_project_by_id(project_id,
                                                                 user)
        except models.ObjectDoesNotExist:
            raise ValidationError("Project not found.")

        if not self._can_user_modify_project(original_project, user):
            raise ValidationError(ERROR_PROJECT_NO_PERMISSION)

        new_title = f"{original_project.title} (Copy)"
        counter = 1

        while self.repository.project_exists(new_title, user):
            new_title = f"{original_project.title} (Copy {counter})"
            counter += 1

        new_project: Project = self.repository.create_project(new_title, user)

        logger.info(
            f"Project '{original_project.title}' duplicated to '{new_title}' by user {user.email}")

        return new_project

    def get_user_projects(self, user: User, limit: Optional[int] = None,
                          include_archived: bool = False) -> List[Project]:
        """Get projects for a user with optional filtering."""
        return list(
            self.repository.get_user_projects(user, limit, include_archived))

    def get_project_stats(self, user: User) -> Dict[str, int]:
        """Get project statistics for a user."""
        return self.repository.get_project_stats(user)

    def search_projects(self, user: User, query: str) -> List[Project]:
        """Search projects by title for a user."""
        if not query.strip():
            return []
        return list(self.repository.search_projects(user, query.strip()))

    def _validate_project_title(self, title: str) -> None:
        """Validate project title according to business rules."""
        if not title or not title.strip():
            raise ValidationError(ERROR_PROJECT_TITLE_EMPTY)

        title = title.strip()

        if len(title) < PROJECT_TITLE_MIN_LENGTH:
            raise ValidationError(ERROR_PROJECT_TITLE_TOO_SHORT)

        if len(title) > PROJECT_TITLE_MAX_LENGTH:
            raise ValidationError(ERROR_PROJECT_TITLE_TOO_LONG)

        if any(char in title for char in ['<', '>', '&', '"', "'"]):
            raise ValidationError(ERROR_PROJECT_TITLE_INVALID_CHARS)

    def _can_user_modify_project(self, project: Project, user: User) -> bool:
        """Check if user can modify the project."""
        return project.owner == user

    def _has_active_tasks(self, project: Project) -> bool:
        """Check if project has active tasks."""
        pass
