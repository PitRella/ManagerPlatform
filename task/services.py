import logging
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

from task.repositories import TaskRepository
from task.models import Task
from task.constants import (
    TASK_TEXT_MIN_LENGTH,
    TASK_TEXT_MAX_LENGTH,
    TASK_PRIORITY_MIN,
    TASK_PRIORITY_MAX,
    ERROR_TASK_TEXT_EMPTY,
    ERROR_TASK_TEXT_TOO_SHORT,
    ERROR_TASK_TEXT_TOO_LONG,
    ERROR_TASK_TEXT_INVALID_CHARS,
    ERROR_TASK_NOT_FOUND,
    ERROR_TASK_NO_PERMISSION,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_TASK_PRIORITY_INVALID,
    ERROR_TASK_REORDER_FAILED,
    ERROR_TASK_TOGGLE_FAILED,
)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()

logger = logging.getLogger(__name__)


class TaskService:
    """Service layer for Task business logic."""

    def __init__(
            self,
            repository: Optional[TaskRepository] = None):
        self.repository = repository or TaskRepository()

    def create_task(
            self,
            text: str,
            project_id: int,
            user: User,
            priority: Optional[int] = None
    ) -> Task:
        """Create a new task with business logic validation."""
        self._validate_task_text(text)
        self._validate_task_priority(priority)

        try:
            task: Task = self.repository.create_task(
                text=text,
                project_id=project_id,
                user=user,
                priority=priority
            )

            logger.info(f"Task '{text}' created in project {project_id} by user {user.email}")

            return task
        except models.ObjectDoesNotExist:
            raise ValidationError(ERROR_PROJECT_NOT_FOUND)

    def update_task(
            self,
            task_id: int,
            user: User,
            **kwargs
    ) -> Task:
        """Update an existing task with business logic validation."""
        try:
            task: Task = self.repository.get_task_by_id(task_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError(ERROR_TASK_NOT_FOUND)

        if not self._can_user_modify_task(task, user):
            raise ValidationError(ERROR_TASK_NO_PERMISSION)

        # Validate text if it's being updated
        if 'text' in kwargs:
            self._validate_task_text(kwargs['text'])

        # Validate priority if it's being updated
        if 'priority' in kwargs:
            self._validate_task_priority(kwargs['priority'])

        updated_task = self.repository.update_task(task_id, user, **kwargs)

        logger.info(f"Task {task_id} updated by user {user.email}")

        return updated_task

    def delete_task(
            self,
            task_id: int,
            user: User
    ) -> bool:
        """Delete a task with business logic validation."""
        try:
            task: Task = self.repository.get_task_by_id(task_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError(ERROR_TASK_NOT_FOUND)

        if not self._can_user_modify_task(task, user):
            raise ValidationError(ERROR_TASK_NO_PERMISSION)

        task_text = task.text
        result = self.repository.delete_task(task_id, user)

        logger.info(f"Task '{task_text}' deleted by user {user.email}")

        return result

    def toggle_task_completion(
            self,
            task_id: int,
            user: User,
            completed: bool
    ) -> Task:
        """Toggle task completion status with business logic validation."""
        try:
            task: Task = self.repository.get_task_by_id(task_id, user)
        except models.ObjectDoesNotExist:
            raise ValidationError(ERROR_TASK_NOT_FOUND)

        if not self._can_user_modify_task(task, user):
            raise ValidationError(ERROR_TASK_NO_PERMISSION)

        try:
            updated_task = self.repository.toggle_task_completion(
                task_id, user, completed
            )

            logger.info(f"Task {task_id} completion toggled to {completed} by user {user.email}")

            return updated_task
        except Exception as e:
            logger.error(f"Failed to toggle task completion: {e}")
            raise ValidationError(ERROR_TASK_TOGGLE_FAILED)

    def reorder_tasks(
            self,
            order_data: List[dict],
            user: User
    ) -> bool:
        """Reorder tasks with business logic validation."""
        if not order_data:
            raise ValidationError("Order data cannot be empty")
        try:
            result = self.repository.reorder_tasks(order_data, user)
            logger.info(f"Tasks reordered by user %s",user.email)
            return result
        except Exception as e:
            logger.error(f"Failed to reorder tasks: %s", e)
            raise ValidationError(ERROR_TASK_REORDER_FAILED) from None

    def get_project_tasks(
            self,
            project_id: int,
            user: User,
            limit: Optional[int] = None
    ) -> List[Task]:
        """Get tasks for a project with optional filtering."""
        return list(self.repository.get_project_tasks(project_id, user, limit))

    def get_task_stats(
            self,
            project_id: int,
            user: User
    ) -> Dict[str, Any]:
        """Get task statistics for a project."""
        return self.repository.get_task_stats(project_id, user)

    def _validate_task_text(self, text: str) -> None:
        """Validate task text according to business rules."""
        if not text or not text.strip():
            raise ValidationError(ERROR_TASK_TEXT_EMPTY)

        text = text.strip()

        if len(text) < TASK_TEXT_MIN_LENGTH:
            raise ValidationError(ERROR_TASK_TEXT_TOO_SHORT)

        if len(text) > TASK_TEXT_MAX_LENGTH:
            raise ValidationError(ERROR_TASK_TEXT_TOO_LONG)

        if any(char in text for char in ['<', '>', '&', '"', "'"]):
            raise ValidationError(ERROR_TASK_TEXT_INVALID_CHARS)

    def _validate_task_priority(self, priority: Optional[int]) -> None:
        """Validate task priority according to business rules."""
        if priority is not None:
            if not isinstance(priority, int):
                raise ValidationError("Priority must be an integer")
            
            if priority < TASK_PRIORITY_MIN or priority > TASK_PRIORITY_MAX:
                raise ValidationError(ERROR_TASK_PRIORITY_INVALID)

    def _can_user_modify_task(self, task: Task, user: User) -> bool:
        """Check if user can modify the task."""
        return task.project.owner == user
