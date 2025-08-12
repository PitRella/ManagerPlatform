from typing import TYPE_CHECKING
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from django.urls import reverse

from task.admin import TaskAdmin
from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskAdminTest(TestCase):
    """Test cases for Task admin interface."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client: Client = Client()
        self.user: User = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.project: Project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            priority=1
        )
        self.admin: TaskAdmin = TaskAdmin(Task, site)

    def test_task_admin_registration(self) -> None:
        """Test that Task model is registered in admin."""
        self.assertIn(Task, site._registry)

    def test_task_admin_list_display(self) -> None:
        """Test TaskAdmin list_display configuration."""
        expected_fields: list[str] = ['text', 'priority', 'completed', 'project']
        
        for field in expected_fields:
            self.assertIn(field, self.admin.list_display)

    def test_task_admin_list_filter(self) -> None:
        """Test TaskAdmin list_filter configuration."""
        expected_filters: list[str] = ['completed', 'project']
        
        for filter_field in expected_filters:
            self.assertIn(filter_field, self.admin.list_filter)

    def test_task_admin_search_fields(self) -> None:
        """Test TaskAdmin search_fields configuration."""
        expected_search_fields: list[str] = ['text']
        
        for field in expected_search_fields:
            self.assertIn(field, self.admin.search_fields)

    def test_task_admin_ordering(self) -> None:
        """Test TaskAdmin ordering configuration."""
        expected_ordering: list[str] = ['-priority']
        
        self.assertEqual(self.admin.ordering, expected_ordering)

    def test_task_admin_readonly_fields(self) -> None:
        """Test TaskAdmin readonly_fields configuration."""
        # Check if readonly_fields is defined (even if empty)
        self.assertTrue(hasattr(self.admin, 'readonly_fields'))

    def test_task_admin_fieldsets(self) -> None:
        """Test TaskAdmin fieldsets configuration."""
        # Check if fieldsets is defined
        self.assertTrue(hasattr(self.admin, 'fieldsets'))

    def test_admin_list_view_accessible(self) -> None:
        """Test that admin list view is accessible to staff users."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_admin_add_view_accessible(self) -> None:
        """Test that admin add view is accessible to staff users."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_admin_change_view_accessible(self) -> None:
        """Test that admin change view is accessible to staff users."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_change', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_admin_delete_view_accessible(self) -> None:
        """Test that admin delete view is accessible to staff users."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_delete', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_admin_list_view_unauthorized(self) -> None:
        """Test that admin list view is not accessible to non-staff users."""
        non_staff_user: User = User.objects.create_user(
            username='nonstaffuser1',
            email='nonstaff@example.com',
            password='testpass123',
            is_staff=False
        )
        self.client.force_login(non_staff_user)
        url: str = reverse('admin:task_task_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)

    def test_admin_add_view_unauthorized(self) -> None:
        """Test that admin add view is not accessible to non-staff users."""
        non_staff_user: User = User.objects.create_user(
            username='nonstaffuser2',
            email='nonstaff@example.com',
            password='testpass123',
            is_staff=False
        )
        self.client.force_login(non_staff_user)
        url: str = reverse('admin:task_task_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)

    def test_admin_change_view_unauthorized(self) -> None:
        """Test that admin change view is not accessible to non-staff users."""
        non_staff_user: User = User.objects.create_user(
            username='nonstaffuser3',
            email='nonstaff@example.com',
            password='testpass123',
            is_staff=False
        )
        self.client.force_login(non_staff_user)
        url: str = reverse('admin:task_task_change', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)

    def test_admin_delete_view_unauthorized(self) -> None:
        """Test that admin delete view is not accessible to non-staff users."""
        non_staff_user: User = User.objects.create_user(
            username='nonstaffuser4',
            email='nonstaff@example.com',
            password='testpass123',
            is_staff=False
        )
        self.client.force_login(non_staff_user)
        url: str = reverse('admin:task_task_delete', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)

    def test_admin_list_view_unauthenticated(self) -> None:
        """Test that admin list view redirects unauthenticated users."""
        url: str = reverse('admin:task_task_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_add_view_unauthenticated(self) -> None:
        """Test that admin add view redirects unauthenticated users."""
        url: str = reverse('admin:task_task_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_change_view_unauthenticated(self) -> None:
        """Test that admin change view redirects unauthenticated users."""
        url: str = reverse('admin:task_task_change', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_delete_view_unauthenticated(self) -> None:
        """Test that admin delete view redirects unauthenticated users."""
        url: str = reverse('admin:task_task_delete', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_create_task(self) -> None:
        """Test creating a task through admin interface."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_add')
        
        data: dict = {
            'text': 'Admin created task',
            'priority': 5,
            'completed': False,
            'project': self.project.id
        }
        
        response = self.client.post(url, data=data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify task was created
        self.assertTrue(Task.objects.filter(text='Admin created task').exists())

    def test_admin_update_task(self) -> None:
        """Test updating a task through admin interface."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_change', args=[self.task.id])
        
        data: dict = {
            'text': 'Updated task text',
            'priority': 10,
            'completed': True,
            'project': self.project.id
        }
        
        response = self.client.post(url, data=data)
        
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        
        # Verify task was updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.text, 'Updated task text')
        self.assertEqual(self.task.priority, 10)
        self.assertTrue(self.task.completed)

    def test_admin_delete_task(self) -> None:
        """Test deleting a task through admin interface."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_delete', args=[self.task.id])
        
        response = self.client.post(url, data={'post': 'yes'})
        
        # Should redirect after successful deletion
        self.assertEqual(response.status_code, 302)
        
        # Verify task was deleted
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_admin_list_view_content(self) -> None:
        """Test that admin list view displays task information."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Check that task information is displayed
        self.assertContains(response, self.task.text)
        self.assertContains(response, str(self.task.priority))
        self.assertContains(response, self.task.project.title)

    def test_admin_change_view_content(self) -> None:
        """Test that admin change view displays task form."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_change', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Check that form fields are present
        self.assertContains(response, 'name="text"')
        self.assertContains(response, 'name="priority"')
        self.assertContains(response, 'name="completed"')
        self.assertContains(response, 'name="project"')
        
        # Check that current values are displayed
        self.assertContains(response, self.task.text)
        self.assertContains(response, str(self.task.priority))

    def test_admin_add_view_content(self) -> None:
        """Test that admin add view displays empty task form."""
        self.client.force_login(self.user)
        url: str = reverse('admin:task_task_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Check that form fields are present
        self.assertContains(response, 'name="text"')
        self.assertContains(response, 'name="priority"')
        self.assertContains(response, 'name="completed"')
        self.assertContains(response, 'name="project"')

    def test_admin_model_verbose_names(self) -> None:
        """Test that admin uses correct verbose names."""
        self.assertEqual(Task._meta.verbose_name, 'Task')
        self.assertEqual(Task._meta.verbose_name_plural, 'Tasks')

    def test_admin_model_meta_options(self) -> None:
        """Test that admin respects model meta options."""
        # Test ordering
        self.assertEqual(Task._meta.ordering, ['-priority'])
        
        # Test db_table
        self.assertEqual(Task._meta.db_table, 'tasks')
