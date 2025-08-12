from typing import TYPE_CHECKING
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from task.repositories import TaskRepository
from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskRepositoryTest(TestCase):
    """Test cases for TaskRepository."""

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
        self.repository: TaskRepository = TaskRepository()

    def test_create_task_with_priority(self) -> None:
        """Test creating task with specified priority."""
        task: Task = self.repository.create_task(
            text='Test task',
            project_id=self.project.id,
            user=self.user,
            priority=5
        )
        
        self.assertEqual(task.text, 'Test task')
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.project, self.project)

    def test_create_task_without_priority(self) -> None:
        """Test creating task without priority (should auto-assign)."""
        task1: Task = self.repository.create_task(
            text='First task',
            project_id=self.project.id,
            user=self.user
        )
        task2: Task = self.repository.create_task(
            text='Second task',
            project_id=self.project.id,
            user=self.user
        )
        
        self.assertEqual(task1.priority, 1)
        self.assertEqual(task2.priority, 2)

    def test_create_task_project_not_found(self) -> None:
        """Test creating task with non-existent project."""
        with self.assertRaises(ObjectDoesNotExist):
            self.repository.create_task(
                text='Test task',
                project_id=999,
                user=self.user
            )

    def test_create_task_wrong_user(self) -> None:
        """Test creating task for project owned by different user."""
        with self.assertRaises(ObjectDoesNotExist):
            self.repository.create_task(
                text='Test task',
                project_id=self.project.id,
                user=self.other_user
            )

    def test_get_task_by_id(self) -> None:
        """Test getting task by ID."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        retrieved_task: Task = self.repository.get_task_by_id(
            task.id, self.user
        )
        self.assertEqual(retrieved_task, task)

    def test_get_task_by_id_not_found(self) -> None:
        """Test getting non-existent task."""
        with self.assertRaises(ObjectDoesNotExist):
            self.repository.get_task_by_id(999, self.user)

    def test_get_task_by_id_wrong_user(self) -> None:
        """Test getting task owned by different user."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        with self.assertRaises(ObjectDoesNotExist):
            self.repository.get_task_by_id(task.id, self.other_user)

    def test_get_project_tasks(self) -> None:
        """Test getting tasks for a project."""
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
        Task.objects.create(
            text='Other task',
            project=self.other_project
        )
        
        tasks = self.repository.get_project_tasks(
            self.project.id, self.user
        )
        
        self.assertEqual(len(tasks), 2)
        self.assertIn(task1, tasks)
        self.assertIn(task2, tasks)

    def test_get_project_tasks_with_limit(self) -> None:
        """Test getting tasks with limit."""
        Task.objects.create(text='Task 1', project=self.project, priority=1)
        Task.objects.create(text='Task 2', project=self.project, priority=2)
        Task.objects.create(text='Task 3', project=self.project, priority=3)
        
        tasks = self.repository.get_project_tasks(
            self.project.id, self.user, limit=2
        )
        
        self.assertEqual(len(tasks), 2)

    def test_get_project_tasks_empty(self) -> None:
        """Test getting tasks for empty project."""
        tasks = self.repository.get_project_tasks(
            self.project.id, self.user
        )
        
        self.assertEqual(len(tasks), 0)

    def test_update_task(self) -> None:
        """Test updating task."""
        task: Task = Task.objects.create(
            text='Original text',
            project=self.project,
            priority=1
        )
        
        updated_task: Task = self.repository.update_task(
            task.id, self.user,
            text='Updated text',
            priority=5
        )
        
        self.assertEqual(updated_task.text, 'Updated text')
        self.assertEqual(updated_task.priority, 5)

    def test_delete_task(self) -> None:
        """Test deleting task."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        result: bool = self.repository.delete_task(task.id, self.user)
        
        self.assertTrue(result)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_exists(self) -> None:
        """Test checking if task exists."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project
        )
        
        self.assertTrue(self.repository.task_exists(task.id, self.user))
        self.assertFalse(self.repository.task_exists(999, self.user))

    def test_get_project_max_priority(self) -> None:
        """Test getting max priority for project."""
        Task.objects.create(text='Task 1', project=self.project, priority=1)
        Task.objects.create(text='Task 2', project=self.project, priority=5)
        Task.objects.create(text='Task 3', project=self.project, priority=3)
        
        max_priority: int = self.repository.get_project_max_priority(
            self.project.id, self.user
        )
        
        self.assertEqual(max_priority, 5)

    def test_get_project_max_priority_empty(self) -> None:
        """Test getting max priority for empty project."""
        max_priority: int = self.repository.get_project_max_priority(
            self.project.id, self.user
        )
        
        self.assertEqual(max_priority, 0)

    def test_toggle_task_completion(self) -> None:
        """Test toggling task completion."""
        task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            completed=False
        )
        
        # Toggle to completed
        updated_task: Task = self.repository.toggle_task_completion(
            task.id, self.user, True
        )
        self.assertTrue(updated_task.completed)
        
        # Toggle back to not completed
        updated_task = self.repository.toggle_task_completion(
            task.id, self.user, False
        )
        self.assertFalse(updated_task.completed)

    def test_reorder_tasks(self) -> None:
        """Test reordering tasks."""
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
        
        result: bool = self.repository.reorder_tasks(order_data, self.user)
        
        self.assertTrue(result)
        
        # Refresh from database
        task1.refresh_from_db()
        task2.refresh_from_db()
        
        self.assertEqual(task1.priority, 5)
        self.assertEqual(task2.priority, 1)

    def test_get_task_stats(self) -> None:
        """Test getting task statistics."""
        Task.objects.create(text='Task 1', project=self.project, completed=False)
        Task.objects.create(text='Task 2', project=self.project, completed=True)
        Task.objects.create(text='Task 3', project=self.project, completed=True)
        
        stats: dict = self.repository.get_task_stats(self.project.id, self.user)
        
        self.assertEqual(stats['total_tasks'], 3)
        self.assertEqual(stats['completed_tasks'], 2)
        self.assertEqual(stats['active_tasks'], 1)
        self.assertEqual(stats['completion_rate'], 66.66666666666667)

    def test_get_task_stats_empty(self) -> None:
        """Test getting task statistics for empty project."""
        stats: dict = self.repository.get_task_stats(self.project.id, self.user)
        
        self.assertEqual(stats['total_tasks'], 0)
        self.assertEqual(stats['completed_tasks'], 0)
        self.assertEqual(stats['active_tasks'], 0)
        self.assertEqual(stats['completion_rate'], 0)
