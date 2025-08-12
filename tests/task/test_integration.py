from typing import TYPE_CHECKING
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskCRUDIntegrationTest(TestCase):
    """Integration tests for complete CRUD operations on tasks."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client: Client = Client()
        self.user: User = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.project: Project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )

    def test_complete_task_lifecycle(self) -> None:
        """Test complete task lifecycle: Create -> Read -> Update -> Delete."""
        self.client.force_login(self.user)
        
        # 1. CREATE - Create a new task
        create_data: dict = {
            'text': 'Integration test task',
            'priority': 5
        }
        create_response = self.client.post(
            reverse('task:create', kwargs={'project_id': self.project.id}),
            data=create_data
        )
        
        self.assertEqual(create_response.status_code, 302)  # Redirect after success
        
        # Verify task was created
        task: Task = Task.objects.get(text='Integration test task')
        self.assertEqual(task.text, 'Integration test task')
        self.assertEqual(task.priority, 5)
        self.assertFalse(task.completed)
        self.assertEqual(task.project, self.project)
        
        # 2. READ - Verify task exists and can be accessed
        self.assertTrue(Task.objects.filter(id=task.id).exists())
        
        # 3. UPDATE - Update the task
        update_data: dict = {
            'text': 'Updated integration test task',
            'priority': 10
        }
        update_response = self.client.post(
            reverse('task:update', kwargs={'task_id': task.id}),
            data=update_data
        )
        
        self.assertEqual(update_response.status_code, 302)  # Redirect after success
        
        # Verify task was updated
        task.refresh_from_db()
        self.assertEqual(task.text, 'Updated integration test task')
        self.assertEqual(task.priority, 10)
        
        # 4. TOGGLE - Toggle task completion
        toggle_response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': task.id}),
            data={'completed': 'true'}
        )
        
        self.assertEqual(toggle_response.status_code, 200)
        task.refresh_from_db()
        self.assertTrue(task.completed)
        
        # Toggle back to not completed
        toggle_response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': task.id}),
            data={'completed': 'false'}
        )
        
        self.assertEqual(toggle_response.status_code, 200)
        task.refresh_from_db()
        self.assertFalse(task.completed)
        
        # 5. DELETE - Delete the task
        delete_response = self.client.post(
            reverse('task:delete', kwargs={'task_id': task.id})
        )
        
        self.assertEqual(delete_response.status_code, 302)  # Redirect after success
        
        # Verify task was deleted
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_multiple_tasks_operations(self) -> None:
        """Test operations with multiple tasks."""
        self.client.force_login(self.user)
        
        # Create multiple tasks
        tasks_data: list[dict] = [
            {'text': 'Task 1', 'priority': 1},
            {'text': 'Task 2', 'priority': 2},
            {'text': 'Task 3', 'priority': 3}
        ]
        
        created_tasks: list[Task] = []
        for data in tasks_data:
            response = self.client.post(
                reverse('task:create', kwargs={'project_id': self.project.id}),
                data=data
            )
            self.assertEqual(response.status_code, 302)
            task = Task.objects.get(text=data['text'])
            created_tasks.append(task)
        
        # Verify all tasks were created
        self.assertEqual(Task.objects.filter(project=self.project).count(), 3)
        
        # Test reordering tasks
        order_data: dict = {
            'order_data': [
                {'id': created_tasks[0].id, 'position': 5},
                {'id': created_tasks[1].id, 'position': 1},
                {'id': created_tasks[2].id, 'position': 3}
            ]
        }
        
        reorder_response = self.client.post(
            reverse('task:reorder'),
            data=order_data,
            content_type='application/json'
        )
        
        self.assertEqual(reorder_response.status_code, 200)
        
        # Verify reordering worked
        for task in created_tasks:
            task.refresh_from_db()
        
        self.assertEqual(created_tasks[0].priority, 5)
        self.assertEqual(created_tasks[1].priority, 1)
        self.assertEqual(created_tasks[2].priority, 3)
        
        # Test bulk operations
        for task in created_tasks:
            # Toggle completion
            self.client.post(
                reverse('task:toggle', kwargs={'task_id': task.id}),
                data={'completed': 'true'}
            )
            task.refresh_from_db()
            self.assertTrue(task.completed)
        
        # Verify all tasks are completed
        self.assertEqual(
            Task.objects.filter(project=self.project, completed=True).count(), 3
        )

    def test_task_permissions_integration(self) -> None:
        """Test task permissions across different users."""
        other_user: User = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_project: Project = Project.objects.create(
            title='Other Project',
            owner=other_user
        )
        
        # User creates task in their project
        self.client.force_login(self.user)
        task_data: dict = {'text': 'User task', 'priority': 1}
        response = self.client.post(
            reverse('task:create', kwargs={'project_id': self.project.id}),
            data=task_data
        )
        self.assertEqual(response.status_code, 302)
        
        user_task: Task = Task.objects.get(text='User task')
        
        # Other user cannot access user's task
        self.client.force_login(other_user)
        
        # Cannot update
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': user_task.id})
        )
        self.assertEqual(response.status_code, 404)
        
        # Cannot delete
        response = self.client.get(
            reverse('task:delete', kwargs={'task_id': user_task.id})
        )
        self.assertEqual(response.status_code, 404)
        
        # Cannot toggle
        response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': user_task.id}),
            data={'completed': 'true'}
        )
        self.assertEqual(response.status_code, 404)
        
        # Other user can create task in their own project
        other_task_data: dict = {'text': 'Other user task', 'priority': 1}
        response = self.client.post(
            reverse('task:create', kwargs={'project_id': other_project.id}),
            data=other_task_data
        )
        self.assertEqual(response.status_code, 302)
        
        other_task: Task = Task.objects.get(text='Other user task')
        
        # Original user cannot access other user's task
        self.client.force_login(self.user)
        
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': other_task.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_task_validation_integration(self) -> None:
        """Test task validation across the entire stack."""
        self.client.force_login(self.user)
        
        # Test invalid text
        invalid_data: list[dict] = [
            {'text': '', 'priority': 1},  # Empty text
            {'text': 'a' * 65, 'priority': 1},  # Too long
            {'text': '<script>alert("xss")</script>', 'priority': 1},  # Invalid chars
        ]
        
        for data in invalid_data:
            response = self.client.post(
                reverse('task:create', kwargs={'project_id': self.project.id}),
                data=data
            )
            self.assertEqual(response.status_code, 200)  # Form errors
            self.assertFalse(Task.objects.filter(text=data['text']).exists())
        
        # Test invalid priority
        invalid_priority_data: list[dict] = [
            {'text': 'Valid task', 'priority': 0},  # Too low
            {'text': 'Valid task', 'priority': 1001},  # Too high
            {'text': 'Valid task', 'priority': -1},  # Negative
        ]
        
        for data in invalid_priority_data:
            response = self.client.post(
                reverse('task:create', kwargs={'project_id': self.project.id}),
                data=data
            )
            self.assertEqual(response.status_code, 200)  # Form errors
            self.assertFalse(Task.objects.filter(text=data['text']).exists())

    def test_task_statistics_integration(self) -> None:
        """Test task statistics functionality."""
        self.client.force_login(self.user)
        
        # Create tasks with different completion statuses
        tasks_data: list[dict] = [
            {'text': 'Active task 1', 'priority': 1},
            {'text': 'Active task 2', 'priority': 2},
            {'text': 'Completed task 1', 'priority': 3},
            {'text': 'Completed task 2', 'priority': 4},
        ]
        
        created_tasks: list[Task] = []
        for data in tasks_data:
            response = self.client.post(
                reverse('task:create', kwargs={'project_id': self.project.id}),
                data=data
            )
            self.assertEqual(response.status_code, 302)
            task = Task.objects.get(text=data['text'])
            created_tasks.append(task)
        
        # Complete some tasks
        for task in created_tasks[2:]:  # Last two tasks
            self.client.post(
                reverse('task:toggle', kwargs={'task_id': task.id}),
                data={'completed': 'true'}
            )
        
        # Verify statistics
        total_tasks = Task.objects.filter(project=self.project).count()
        completed_tasks = Task.objects.filter(project=self.project, completed=True).count()
        active_tasks = Task.objects.filter(project=self.project, completed=False).count()
        
        self.assertEqual(total_tasks, 4)
        self.assertEqual(completed_tasks, 2)
        self.assertEqual(active_tasks, 2)
        self.assertEqual(completed_tasks / total_tasks * 100, 50.0)  # 50% completion rate
