from typing import TYPE_CHECKING
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskModelTest(TestCase):
    """Test cases for Task model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user: User = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project: Project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )

    def test_task_creation(self) -> None:
        """Test basic task creation."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            priority=1
        )
        
        self.assertEqual(task.text, 'Test task')
        self.assertEqual(task.priority, 1)
        self.assertFalse(task.completed)
        self.assertEqual(task.project, self.project)

    def test_task_string_representation(self) -> None:
        """Test task string representation."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        self.assertEqual(str(task), 'Test task')

    def test_task_default_values(self) -> None:
        """Test task default values."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        self.assertEqual(task.priority, 1)
        self.assertFalse(task.completed)

    def test_task_ordering(self) -> None:
        """Test task ordering by priority."""
        task1: Task = Task.objects.create(
            text='Low priority task',
            project=self.project,
            priority=1
        )
        task2: Task = Task.objects.create(
            text='High priority task',
            project=self.project,
            priority=3
        )
        task3: Task = Task.objects.create(
            text='Medium priority task',
            project=self.project,
            priority=2
        )
        
        tasks: list[Task] = list(Task.objects.all())
        self.assertEqual(tasks[0], task2)  # Highest priority first
        self.assertEqual(tasks[1], task3)
        self.assertEqual(tasks[2], task1)

    def test_task_foreign_key_relationship(self) -> None:
        """Test task-project relationship."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        self.assertEqual(task.project, self.project)
        self.assertIn(task, self.project.tasks.all())

    def test_task_cascade_delete(self) -> None:
        """Test that tasks are deleted when project is deleted."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        self.project.delete()
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_priority_validation(self) -> None:
        """Test task priority validation."""
        # Test valid priority
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            priority=100
        )
        self.assertEqual(task.priority, 100)

    def test_task_text_max_length(self) -> None:
        """Test task text max length constraint."""
        long_text: str = 'a' * 64  # Exactly at the limit
        task: Task = Task.objects.create(
            text=long_text,
            project=self.project
        )
        self.assertEqual(task.text, long_text)

    def test_task_meta_options(self) -> None:
        """Test task meta options."""
        self.assertEqual(Task._meta.db_table, 'tasks')
        self.assertEqual(Task._meta.verbose_name, 'Task')
        self.assertEqual(Task._meta.verbose_name_plural, 'Tasks')
        self.assertEqual(Task._meta.ordering, ['-priority'])
