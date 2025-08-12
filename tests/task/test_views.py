from typing import TYPE_CHECKING
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskViewsTest(TestCase):
    """Test cases for Task views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client: Client = Client()
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
        self.task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            priority=1
        )

    def test_create_task_view_get(self) -> None:
        """Test GET request to create task view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('task:create', kwargs={'project_id': self.project.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_create_task_view_post_valid(self) -> None:
        """Test POST request to create task view with valid data."""
        self.client.force_login(self.user)
        data: dict = {
            'text': 'New task',
            'priority': 5
        }
        response = self.client.post(
            reverse('task:create', kwargs={'project_id': self.project.id}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Task.objects.filter(text='New task').exists())

    def test_create_task_view_post_invalid(self) -> None:
        """Test POST request to create task view with invalid data."""
        self.client.force_login(self.user)
        data: dict = {
            'text': '',  # Empty text
            'priority': 1
        }
        response = self.client.post(
            reverse('task:create', kwargs={'project_id': self.project.id}),
            data=data
        )
        
        self.assertEqual(response.status_code, 200)  # Form errors
        self.assertFalse(Task.objects.filter(text='').exists())

    def test_create_task_view_unauthorized(self) -> None:
        """Test create task view without authentication."""
        response = self.client.get(
            reverse('task:create', kwargs={'project_id': self.project.id})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_task_view_wrong_user(self) -> None:
        """Test create task view for project owned by different user."""
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('task:create', kwargs={'project_id': self.project.id})
        )
        
        self.assertEqual(response.status_code, 404)

    def test_update_task_view_get(self) -> None:
        """Test GET request to update task view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_update_task_view_post_valid(self) -> None:
        """Test POST request to update task view with valid data."""
        self.client.force_login(self.user)
        data: dict = {
            'text': 'Updated task',
            'priority': 10
        }
        response = self.client.post(
            reverse('task:update', kwargs={'task_id': self.task.id}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.task.refresh_from_db()
        self.assertEqual(self.task.text, 'Updated task')
        self.assertEqual(self.task.priority, 10)

    def test_update_task_view_post_invalid(self) -> None:
        """Test POST request to update task view with invalid data."""
        self.client.force_login(self.user)
        data: dict = {
            'text': '',  # Empty text
            'priority': 1
        }
        response = self.client.post(
            reverse('task:update', kwargs={'task_id': self.task.id}),
            data=data
        )
        
        self.assertEqual(response.status_code, 200)  # Form errors
        self.task.refresh_from_db()
        self.assertEqual(self.task.text, 'Test task')  # Unchanged

    def test_update_task_view_unauthorized(self) -> None:
        """Test update task view without authentication."""
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_update_task_view_wrong_user(self) -> None:
        """Test update task view for task owned by different user."""
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 404)

    def test_delete_task_view_get(self) -> None:
        """Test GET request to delete task view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('task:delete', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/delete.html')

    def test_delete_task_view_post(self) -> None:
        """Test POST request to delete task view."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('task:delete', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_view_unauthorized(self) -> None:
        """Test delete task view without authentication."""
        response = self.client.get(
            reverse('task:delete', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_delete_task_view_wrong_user(self) -> None:
        """Test delete task view for task owned by different user."""
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('task:delete', kwargs={'task_id': self.task.id})
        )
        
        self.assertEqual(response.status_code, 404)

    def test_toggle_task_view_post(self) -> None:
        """Test POST request to toggle task view."""
        self.client.force_login(self.user)
        self.assertFalse(self.task.completed)
        
        response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': self.task.id}),
            data={'completed': 'true'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_toggle_task_view_unauthorized(self) -> None:
        """Test toggle task view without authentication."""
        response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': self.task.id}),
            data={'completed': 'true'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_toggle_task_view_wrong_user(self) -> None:
        """Test toggle task view for task owned by different user."""
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': self.task.id}),
            data={'completed': 'true'}
        )
        
        self.assertEqual(response.status_code, 404)

    def test_reorder_tasks_view_post(self) -> None:
        """Test POST request to reorder tasks view."""
        self.client.force_login(self.user)
        task2: Task = Task.objects.create(
            text='Task 2',
            project=self.project,
            priority=2
        )
        
        data: dict = {
            'order_data': [
                {'id': self.task.id, 'position': 5},
                {'id': task2.id, 'position': 1}
            ]
        }
        response = self.client.post(
            reverse('task:reorder'),
            data=data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(self.task.priority, 5)
        self.assertEqual(task2.priority, 1)

    def test_reorder_tasks_view_unauthorized(self) -> None:
        """Test reorder tasks view without authentication."""
        response = self.client.post(reverse('task:reorder'))
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_task_not_found(self) -> None:
        """Test views with non-existent task."""
        self.client.force_login(self.user)
        
        # Test update
        response = self.client.get(
            reverse('task:update', kwargs={'task_id': 999})
        )
        self.assertEqual(response.status_code, 404)
        
        # Test delete
        response = self.client.get(
            reverse('task:delete', kwargs={'task_id': 999})
        )
        self.assertEqual(response.status_code, 404)
        
        # Test toggle
        response = self.client.post(
            reverse('task:toggle', kwargs={'task_id': 999}),
            data={'completed': 'true'}
        )
        self.assertEqual(response.status_code, 404)

    def test_project_not_found(self) -> None:
        """Test create task view with non-existent project."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('task:create', kwargs={'project_id': 999})
        )
        
        self.assertEqual(response.status_code, 404)
