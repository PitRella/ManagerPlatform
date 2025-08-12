from typing import Optional, List, TYPE_CHECKING
from django.db.models import QuerySet, Max
from django.contrib.auth import get_user_model

from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskRepository:
    """Repository for managing Task data access operations."""

    def __init__(self) -> None:
        self.model = Task

    def get_project_tasks(
            self,
            project_id: int,
            user: User,
            limit: Optional[int] = None
    ) -> QuerySet[Task]:
        """Get tasks for a specific project."""
        queryset: QuerySet[Task] = self.model.objects.filter(
            project_id=project_id,
            project__owner=user
        ).order_by('-priority')

        if limit:
            queryset = queryset[:limit]

        return queryset

    def get_task_by_id(
            self,
            task_id: int,
            user: User
    ) -> Task:
        """Get a specific task by ID for a user."""
        return self.model.objects.filter(
            id=task_id,
            project__owner=user
        ).get()

    def create_task(
            self,
            text: str,
            project_id: int,
            user: User,
            priority: Optional[int] = None
    ) -> Task:
        """Create a new task."""
        project = Project.objects.filter(id=project_id, owner=user).get()
        
        if priority is None:
            # Get the highest priority and add 1
            max_priority = self.model.objects.filter(
                project=project
            ).aggregate(Max('priority'))['priority__max'] or 0
            priority = max_priority + 1

        return self.model.objects.create(
            text=text,
            project=project,
            priority=priority
        )

    def update_task(
            self,
            task_id: int,
            user: User,
            **kwargs
    ) -> Task:
        """Update an existing task."""
        task: Task = self.get_task_by_id(task_id, user)
        
        for field, value in kwargs.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        task.save()
        return task

    def delete_task(
            self,
            task_id: int,
            user: User
    ) -> bool:
        """Delete a task."""
        task: Task = self.get_task_by_id(task_id, user)
        task.delete()
        return True

    def task_exists(
            self,
            task_id: int,
            user: User
    ) -> bool:
        """Check if a task exists for a user."""
        return self.model.objects.filter(
            id=task_id,
            project__owner=user
        ).exists()

    def get_project_max_priority(
            self,
            project_id: int,
            user: User
    ) -> int:
        """Get the maximum priority for tasks in a project."""
        max_priority = self.model.objects.filter(
            project_id=project_id,
            project__owner=user
        ).aggregate(Max('priority'))['priority__max']
        return max_priority or 0

    def reorder_tasks(
            self,
            order_data: List[dict],
            user: User
    ) -> bool:
        """Reorder tasks based on provided order data."""
        for item in order_data:
            task_id = item.get('id')
            position = item.get('position')
            
            if task_id and position is not None:
                try:
                    task = self.get_task_by_id(task_id, user)
                    task.priority = int(position)
                    task.save(update_fields=['priority'])
                except (ValueError, self.model.DoesNotExist):
                    continue
        
        return True

    def toggle_task_completion(
            self,
            task_id: int,
            user: User,
            completed: bool
    ) -> Task:
        """Toggle task completion status."""
        task = self.get_task_by_id(task_id, user)
        task.completed = completed
        task.save(update_fields=['completed'])
        return task

    def get_task_stats(
            self,
            project_id: int,
            user: User
    ) -> dict:
        """Get task statistics for a project."""
        tasks = self.model.objects.filter(
            project_id=project_id,
            project__owner=user
        )
        
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        active_tasks = total_tasks - completed_tasks
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'active_tasks': active_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
