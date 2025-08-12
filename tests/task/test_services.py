from typing import TYPE_CHECKING
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from task.services import TaskService
from task.models import Task
from project.models import Project
from task.constants import (
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


class TaskServiceTest(TestCase):
    """Test cases for TaskService."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user: User = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user: User = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.project: Project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.other_project: Project = Project.objects.create(
            title='Other Project',
            owner=self.other_user
        )
        self.service: TaskService = TaskService()

    def test_create_task_success(self) -> None:
        """Test successful task creation."""
        task: Task = self.service.create_task(
            text='Test task',
            project_id=self.project.id,
            user=self.user,
            priority=5
        )
        
        self.assertEqual(task.text, 'Test task')
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.project, self.project)
        self.assertFalse(task.completed)

    def test_create_task_without_priority(self) -> None:
        """Test creating task without priority."""
        task: Task = self.service.create_task(
            text='Test task',
            project_id=self.project.id,
            user=self.user
        )
        
        self.assertEqual(task.text, 'Test task')
        self.assertEqual(task.priority, 1)  # Default priority

    def test_create_task_project_not_found(self) -> None:
        """Test creating task with non-existent project."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='Test task',
                project_id=999,
                user=self.user
            )
        
        self.assertEqual(str(context.exception), ERROR_PROJECT_NOT_FOUND)

    def test_create_task_wrong_user(self) -> None:
        """Test creating task for project owned by different user."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='Test task',
                project_id=self.project.id,
                user=self.other_user
            )
        
        self.assertEqual(str(context.exception), ERROR_PROJECT_NOT_FOUND)

    def test_create_task_empty_text(self) -> None:
        """Test creating task with empty text."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='',
                project_id=self.project.id,
                user=self.user
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_TEXT_EMPTY)

    def test_create_task_whitespace_text(self) -> None:
        """Test creating task with whitespace-only text."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='   ',
                project_id=self.project.id,
                user=self.user
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_TEXT_EMPTY)

    def test_create_task_text_too_short(self) -> None:
        """Test creating task with text that's too short."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='',  # Empty string is less than min length
                project_id=self.project.id,
                user=self.user
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_TEXT_EMPTY)

    def test_create_task_text_too_long(self) -> None:
        """Test creating task with text that's too long."""
        long_text: str = 'a' * 65  # More than max length of 64
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text=long_text,
                project_id=self.project.id,
                user=self.user
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_TEXT_TOO_LONG)

    def test_create_task_invalid_chars(self) -> None:
        """Test creating task with invalid characters."""
        invalid_texts: list[str] = [
            'Task with <script>',
            'Task with >',
            'Task with &',
            'Task with "quotes"',
            "Task with 'quotes'"
        ]
        
        for text in invalid_texts:
            with self.assertRaises(ValidationError) as context:
                self.service.create_task(
                    text=text,
                    project_id=self.project.id,
                    user=self.user
                )
            self.assertEqual(str(context.exception), ERROR_TASK_TEXT_INVALID_CHARS)

    def test_create_task_invalid_priority(self) -> None:
        """Test creating task with invalid priority."""
        # Test priority too low
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='Test task',
                project_id=self.project.id,
                user=self.user,
                priority=0
            )
        self.assertEqual(str(context.exception), ERROR_TASK_PRIORITY_INVALID)
        
        # Test priority too high
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(
                text='Test task',
                project_id=self.project.id,
                user=self.user,
                priority=1001
            )
        self.assertEqual(str(context.exception), ERROR_TASK_PRIORITY_INVALID)

    def test_update_task_success(self) -> None:
        """Test successful task update."""
        task: Task = Task.objects.create(
            text='Original text',
            project=self.project,
            priority=1
        )
        
        updated_task: Task = self.service.update_task(
            task.id, self.user,
            text='Updated text',
            priority=5
        )
        
        self.assertEqual(updated_task.text, 'Updated text')
        self.assertEqual(updated_task.priority, 5)

    def test_update_task_not_found(self) -> None:
        """Test updating non-existent task."""
        with self.assertRaises(ValidationError) as context:
            self.service.update_task(
                999, self.user,
                text='Updated text'
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_NOT_FOUND)

    def test_update_task_no_permission(self) -> None:
        """Test updating task without permission."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        with self.assertRaises(ValidationError) as context:
            self.service.update_task(
                task.id, self.other_user,
                text='Updated text'
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_NO_PERMISSION)

    def test_update_task_invalid_text(self) -> None:
        """Test updating task with invalid text."""
        task: Task = Task.objects.create(
            text='Original text',
            project=self.project
        )
        
        with self.assertRaises(ValidationError) as context:
            self.service.update_task(
                task.id, self.user,
                text='<script>alert("xss")</script>'
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_TEXT_INVALID_CHARS)

    def test_delete_task_success(self) -> None:
        """Test successful task deletion."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        result: bool = self.service.delete_task(task.id, self.user)
        
        self.assertTrue(result)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_not_found(self) -> None:
        """Test deleting non-existent task."""
        with self.assertRaises(ValidationError) as context:
            self.service.delete_task(999, self.user)
        
        self.assertEqual(str(context.exception), ERROR_TASK_NOT_FOUND)

    def test_delete_task_no_permission(self) -> None:
        """Test deleting task without permission."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        with self.assertRaises(ValidationError) as context:
            self.service.delete_task(task.id, self.other_user)
        
        self.assertEqual(str(context.exception), ERROR_TASK_NO_PERMISSION)

    def test_toggle_task_completion_success(self) -> None:
        """Test successful task completion toggle."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            completed=False
        )
        
        # Toggle to completed
        updated_task: Task = self.service.toggle_task_completion(
            task.id, self.user, True
        )
        self.assertTrue(updated_task.completed)
        
        # Toggle back to not completed
        updated_task = self.service.toggle_task_completion(
            task.id, self.user, False
        )
        self.assertFalse(updated_task.completed)

    def test_toggle_task_completion_not_found(self) -> None:
        """Test toggling non-existent task."""
        with self.assertRaises(ValidationError) as context:
            self.service.toggle_task_completion(999, self.user, True)
        
        self.assertEqual(str(context.exception), ERROR_TASK_NOT_FOUND)

    def test_toggle_task_completion_no_permission(self) -> None:
        """Test toggling task without permission."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        with self.assertRaises(ValidationError) as context:
            self.service.toggle_task_completion(
                task.id, self.other_user, True
            )
        
        self.assertEqual(str(context.exception), ERROR_TASK_NO_PERMISSION)

    def test_reorder_tasks_success(self) -> None:
        """Test successful task reordering."""
        task1: Task = Task.objects.create(
            text='Task 1',
            project=self.project,
            priority=1
        )
        task2: Task = Task.objects.create(
            text='Task 2',
            project=self.project,
            priority=2
        )
        
        order_data: list[dict] = [
            {'id': task1.id, 'position': 5},
            {'id': task2.id, 'position': 1}
        ]
        
        result: bool = self.service.reorder_tasks(order_data, self.user)
        
        self.assertTrue(result)
        
        # Refresh from database
        task1.refresh_from_db()
        task2.refresh_from_db()
        
        self.assertEqual(task1.priority, 5)
        self.assertEqual(task2.priority, 1)

    def test_reorder_tasks_empty_data(self) -> None:
        """Test reordering with empty data."""
        with self.assertRaises(ValidationError) as context:
            self.service.reorder_tasks([], self.user)
        
        self.assertEqual(str(context.exception), "Order data cannot be empty")

    def test_get_project_tasks(self) -> None:
        """Test getting project tasks."""
        task1: Task = Task.objects.create(
            text='Task 1',
            project=self.project,
            priority=1
        )
        task2: Task = Task.objects.create(
            text='Task 2',
            project=self.project,
            priority=2
        )
        
        tasks: list[Task] = self.service.get_project_tasks(
            self.project.id, self.user
        )
        
        self.assertEqual(len(tasks), 2)
        self.assertIn(task1, tasks)
        self.assertIn(task2, tasks)

    def test_get_project_tasks_with_limit(self) -> None:
        """Test getting project tasks with limit."""
        Task.objects.create(text='Task 1', project=self.project, priority=1)
        Task.objects.create(text='Task 2', project=self.project, priority=2)
        Task.objects.create(text='Task 3', project=self.project, priority=3)
        
        tasks: list[Task] = self.service.get_project_tasks(
            self.project.id, self.user, limit=2
        )
        
        self.assertEqual(len(tasks), 2)

    def test_get_task_stats(self) -> None:
        """Test getting task statistics."""
        Task.objects.create(text='Task 1', project=self.project, completed=False)
        Task.objects.create(text='Task 2', project=self.project, completed=True)
        Task.objects.create(text='Task 3', project=self.project, completed=True)
        
        stats: dict = self.service.get_task_stats(self.project.id, self.user)
        
        self.assertEqual(stats['total_tasks'], 3)
        self.assertEqual(stats['completed_tasks'], 2)
        self.assertEqual(stats['active_tasks'], 1)
        self.assertEqual(stats['completion_rate'], 66.66666666666667)

    def test_get_task_stats_empty(self) -> None:
        """Test getting task statistics for empty project."""
        stats: dict = self.service.get_task_stats(self.project.id, self.user)
        
        self.assertEqual(stats['total_tasks'], 0)
        self.assertEqual(stats['completed_tasks'], 0)
        self.assertEqual(stats['active_tasks'], 0)
        self.assertEqual(stats['completion_rate'], 0)
