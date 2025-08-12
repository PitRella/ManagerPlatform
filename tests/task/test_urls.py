from typing import TYPE_CHECKING
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from task.views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskToggleView,
    TaskReorderView,
)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskUrlsTest(TestCase):
    """Test cases for Task URL patterns."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user: User = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_task_create_url(self) -> None:
        """Test task create URL pattern."""
        project_id: int = 1
        url: str = reverse('task:create', kwargs={'project_id': project_id})
        
        self.assertEqual(url, f'/task/{project_id}/create/')
        
        # Test URL resolution
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'TaskCreateView')
        self.assertEqual(resolver_match.kwargs['project_id'], str(project_id))

    def test_task_update_url(self) -> None:
        """Test task update URL pattern."""
        task_id: int = 1
        url: str = reverse('task:update', kwargs={'task_id': task_id})
        
        self.assertEqual(url, f'/task/{task_id}/update/')
        
        # Test URL resolution
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'TaskUpdateView')
        self.assertEqual(resolver_match.kwargs['task_id'], str(task_id))

    def test_task_delete_url(self) -> None:
        """Test task delete URL pattern."""
        task_id: int = 1
        url: str = reverse('task:delete', kwargs={'task_id': task_id})
        
        self.assertEqual(url, f'/task/{task_id}/delete/')
        
        # Test URL resolution
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'TaskDeleteView')
        self.assertEqual(resolver_match.kwargs['task_id'], str(task_id))

    def test_task_toggle_url(self) -> None:
        """Test task toggle URL pattern."""
        task_id: int = 1
        url: str = reverse('task:toggle', kwargs={'task_id': task_id})
        
        self.assertEqual(url, f'/task/{task_id}/toggle/')
        
        # Test URL resolution
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'TaskToggleView')
        self.assertEqual(resolver_match.kwargs['task_id'], str(task_id))

    def test_task_reorder_url(self) -> None:
        """Test task reorder URL pattern."""
        url: str = reverse('task:reorder')
        
        self.assertEqual(url, '/task/reorder/')
        
        # Test URL resolution
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'TaskReorderView')

    def test_url_namespace(self) -> None:
        """Test that all task URLs use the correct namespace."""
        urls_to_test: list[tuple[str, dict]] = [
            ('task:create', {'project_id': 1}),
            ('task:update', {'task_id': 1}),
            ('task:delete', {'task_id': 1}),
            ('task:toggle', {'task_id': 1}),
            ('task:reorder', {}),
        ]
        
        for url_name, kwargs in urls_to_test:
            url: str = reverse(url_name, kwargs=kwargs)
            self.assertTrue(url.startswith('/task/'))

    def test_url_parameters(self) -> None:
        """Test URL parameters are correctly handled."""
        # Test with different IDs
        test_ids: list[int] = [1, 100, 999]
        
        for test_id in test_ids:
            # Test create URL
            create_url: str = reverse('task:create', kwargs={'project_id': test_id})
            self.assertIn(str(test_id), create_url)
            
            # Test update URL
            update_url: str = reverse('task:update', kwargs={'task_id': test_id})
            self.assertIn(str(test_id), update_url)
            
            # Test delete URL
            delete_url: str = reverse('task:delete', kwargs={'task_id': test_id})
            self.assertIn(str(test_id), delete_url)
            
            # Test toggle URL
            toggle_url: str = reverse('task:toggle', kwargs={'task_id': test_id})
            self.assertIn(str(test_id), toggle_url)

    def test_url_structure(self) -> None:
        """Test URL structure and format."""
        # Test that URLs follow RESTful conventions
        project_id: int = 1
        task_id: int = 1
        
        create_url: str = reverse('task:create', kwargs={'project_id': project_id})
        update_url: str = reverse('task:update', kwargs={'task_id': task_id})
        delete_url: str = reverse('task:delete', kwargs={'task_id': task_id})
        toggle_url: str = reverse('task:toggle', kwargs={'task_id': task_id})
        reorder_url: str = reverse('task:reorder')
        
        # Check URL structure
        self.assertTrue(create_url.endswith('/'))
        self.assertTrue(update_url.endswith('/'))
        self.assertTrue(delete_url.endswith('/'))
        self.assertTrue(toggle_url.endswith('/'))
        self.assertTrue(reorder_url.endswith('/'))
        
        # Check URL patterns
        self.assertIn('/task/', create_url)
        self.assertIn('/task/', update_url)
        self.assertIn('/task/', delete_url)
        self.assertIn('/task/', toggle_url)
        self.assertIn('/task/', reorder_url)

    def test_url_reverse_consistency(self) -> None:
        """Test that URL reverse and resolve are consistent."""
        project_id: int = 1
        task_id: int = 1
        
        # Test create URL
        create_url: str = reverse('task:create', kwargs={'project_id': project_id})
        create_resolver = resolve(create_url)
        self.assertEqual(create_resolver.kwargs['project_id'], str(project_id))
        
        # Test update URL
        update_url: str = reverse('task:update', kwargs={'task_id': task_id})
        update_resolver = resolve(update_url)
        self.assertEqual(update_resolver.kwargs['task_id'], str(task_id))
        
        # Test delete URL
        delete_url: str = reverse('task:delete', kwargs={'task_id': task_id})
        delete_resolver = resolve(delete_url)
        self.assertEqual(delete_resolver.kwargs['task_id'], str(task_id))
        
        # Test toggle URL
        toggle_url: str = reverse('task:toggle', kwargs={'task_id': task_id})
        toggle_resolver = resolve(toggle_url)
        self.assertEqual(toggle_resolver.kwargs['task_id'], str(task_id))

    def test_url_view_mapping(self) -> None:
        """Test that URLs map to correct view classes."""
        project_id: int = 1
        task_id: int = 1
        
        # Test create URL
        create_url: str = reverse('task:create', kwargs={'project_id': project_id})
        create_resolver = resolve(create_url)
        self.assertEqual(create_resolver.func.__name__, 'TaskCreateView')
        
        # Test update URL
        update_url: str = reverse('task:update', kwargs={'task_id': task_id})
        update_resolver = resolve(update_url)
        self.assertEqual(update_resolver.func.__name__, 'TaskUpdateView')
        
        # Test delete URL
        delete_url: str = reverse('task:delete', kwargs={'task_id': task_id})
        delete_resolver = resolve(delete_url)
        self.assertEqual(delete_resolver.func.__name__, 'TaskDeleteView')
        
        # Test toggle URL
        toggle_url: str = reverse('task:toggle', kwargs={'task_id': task_id})
        toggle_resolver = resolve(toggle_url)
        self.assertEqual(toggle_resolver.func.__name__, 'TaskToggleView')
        
        # Test reorder URL
        reorder_url: str = reverse('task:reorder')
        reorder_resolver = resolve(reorder_url)
        self.assertEqual(reorder_resolver.func.__name__, 'TaskReorderView')

    def test_url_parameter_types(self) -> None:
        """Test URL parameter type handling."""
        # Test with string IDs (should work the same as integers)
        project_id_str: str = "1"
        task_id_str: str = "1"
        
        create_url: str = reverse('task:create', kwargs={'project_id': project_id_str})
        update_url: str = reverse('task:update', kwargs={'task_id': task_id_str})
        
        self.assertIn(project_id_str, create_url)
        self.assertIn(task_id_str, update_url)

    def test_url_uniqueness(self) -> None:
        """Test that all URLs are unique."""
        project_id: int = 1
        task_id: int = 1
        
        urls: list[str] = [
            reverse('task:create', kwargs={'project_id': project_id}),
            reverse('task:update', kwargs={'task_id': task_id}),
            reverse('task:delete', kwargs={'task_id': task_id}),
            reverse('task:toggle', kwargs={'task_id': task_id}),
            reverse('task:reorder'),
        ]
        
        # Check that all URLs are unique
        unique_urls: set[str] = set(urls)
        self.assertEqual(len(urls), len(unique_urls))

    def test_url_http_methods(self) -> None:
        """Test that URLs support appropriate HTTP methods."""
        # This test assumes that the views support GET and POST methods
        # The actual method support would be tested in view tests
        project_id: int = 1
        task_id: int = 1
        
        # All these URLs should be accessible
        urls: list[str] = [
            reverse('task:create', kwargs={'project_id': project_id}),
            reverse('task:update', kwargs={'task_id': task_id}),
            reverse('task:delete', kwargs={'task_id': task_id}),
            reverse('task:toggle', kwargs={'task_id': task_id}),
            reverse('task:reorder'),
        ]
        
        for url in urls:
            # URL should be valid and resolvable
            resolver_match = resolve(url)
            self.assertIsNotNone(resolver_match.func)
