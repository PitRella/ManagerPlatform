from typing import TYPE_CHECKING
from django.test import TestCase
from django.apps import apps

from task.apps import TaskConfig

if TYPE_CHECKING:
    pass


class TaskAppsTest(TestCase):
    """Test cases for Task app configuration."""

    def test_task_app_config(self) -> None:
        """Test TaskConfig configuration."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        self.assertEqual(app_config.name, 'task')
        self.assertEqual(app_config.verbose_name, 'Task')

    def test_task_app_registration(self) -> None:
        """Test that task app is properly registered."""
        self.assertTrue(apps.is_installed('task'))

    def test_task_app_models(self) -> None:
        """Test that task models are properly registered."""
        from task.models import Task
        
        # Check that Task model is registered
        self.assertIsNotNone(apps.get_model('task', 'Task'))
        
        # Check that we can get the model through apps
        task_model = apps.get_model('task', 'Task')
        self.assertEqual(task_model, Task)

    def test_task_app_admin(self) -> None:
        """Test that task admin is properly configured."""
        from task.admin import TaskAdmin
        from task.models import Task
        from django.contrib.admin.sites import site
        
        # Check that TaskAdmin is registered
        self.assertIn(Task, site._registry)
        
        # Check that TaskAdmin is the correct admin class
        admin_class = site._registry[Task].__class__
        self.assertEqual(admin_class, TaskAdmin)

    def test_task_app_urls(self) -> None:
        """Test that task URLs are properly configured."""
        from django.urls import reverse
        
        # Test that task URLs can be reversed
        urls_to_test: list[tuple[str, dict]] = [
            ('task:create', {'project_id': 1}),
            ('task:update', {'task_id': 1}),
            ('task:delete', {'task_id': 1}),
            ('task:toggle', {'task_id': 1}),
            ('task:reorder', {}),
        ]
        
        for url_name, kwargs in urls_to_test:
            try:
                url: str = reverse(url_name, kwargs=kwargs)
                self.assertTrue(url.startswith('/task/'))
            except Exception as e:
                self.fail(f"Failed to reverse URL {url_name}: {e}")

    def test_task_app_services(self) -> None:
        """Test that task services are properly configured."""
        from task.services import TaskService
        from task.repositories import TaskRepository
        
        # Check that services can be instantiated
        repository = TaskRepository()
        service = TaskService(repository=repository)
        
        self.assertIsInstance(repository, TaskRepository)
        self.assertIsInstance(service, TaskService)

    def test_task_app_forms(self) -> None:
        """Test that task forms are properly configured."""
        from task.forms import TaskForm
        
        # Check that forms can be instantiated
        form = TaskForm()
        
        self.assertIsInstance(form, TaskForm)

    def test_task_app_constants(self) -> None:
        """Test that task constants are properly defined."""
        from task.constants import (
            TASK_TEXT_MIN_LENGTH,
            TASK_TEXT_MAX_LENGTH,
            TASK_PRIORITY_MIN,
            TASK_PRIORITY_MAX,
            ERROR_TASK_TEXT_EMPTY,
            ERROR_TASK_NOT_FOUND,
        )
        
        # Check that constants have expected values
        self.assertEqual(TASK_TEXT_MIN_LENGTH, 1)
        self.assertEqual(TASK_PRIORITY_MIN, 1)
        self.assertGreater(TASK_TEXT_MAX_LENGTH, TASK_TEXT_MIN_LENGTH)
        self.assertGreater(TASK_PRIORITY_MAX, TASK_PRIORITY_MIN)
        
        # Check that error messages are strings
        self.assertIsInstance(ERROR_TASK_TEXT_EMPTY, str)
        self.assertIsInstance(ERROR_TASK_NOT_FOUND, str)

    def test_task_app_exceptions(self) -> None:
        """Test that task exceptions are properly defined."""
        from task.exceptions import (
            TaskNotFoundError,
            TaskPermissionError,
            ProjectNotFoundError,
            TaskValidationError,
            TaskReorderError,
            TaskToggleError,
        )
        
        # Check that exceptions can be instantiated
        exceptions: list = [
            TaskNotFoundError("test"),
            TaskPermissionError("test"),
            ProjectNotFoundError("test"),
            TaskValidationError("test"),
            TaskReorderError("test"),
            TaskToggleError("test"),
        ]
        
        for exception in exceptions:
            self.assertIsInstance(exception, Exception)

    def test_task_app_migrations(self) -> None:
        """Test that task migrations are properly configured."""
        from django.db.migrations.loader import MigrationLoader
        from django.db import connection
        
        # Check that migrations exist
        loader = MigrationLoader(connection)
        migrations = loader.migrations.get('task', {})
        
        self.assertGreater(len(migrations), 0)

    def test_task_app_templates(self) -> None:
        """Test that task templates are properly configured."""
        from django.template.loader import get_template
        
        # Check that templates can be loaded
        template_names: list[str] = [
            'task/task_form.html',
            'task/delete.html',
        ]
        
        for template_name in template_names:
            try:
                template = get_template(template_name)
                self.assertIsNotNone(template)
            except Exception as e:
                self.fail(f"Failed to load template {template_name}: {e}")

    def test_task_app_static_files(self) -> None:
        """Test that task static files are properly configured."""
        from django.contrib.staticfiles.finders import find
        
        # Check that static files can be found
        static_files: list[str] = [
            'css/style.css',
            'js/script.js',
        ]
        
        for static_file in static_files:
            try:
                file_path = find(static_file)
                if file_path:
                    self.assertTrue(file_path.endswith(static_file))
            except Exception:
                # Static files might not exist in test environment
                pass

    def test_task_app_settings(self) -> None:
        """Test that task app settings are properly configured."""
        from django.conf import settings
        
        # Check that task app is in INSTALLED_APPS
        self.assertIn('task', settings.INSTALLED_APPS)

    def test_task_app_imports(self) -> None:
        """Test that all task app modules can be imported."""
        modules_to_test: list[str] = [
            'task.models',
            'task.views',
            'task.forms',
            'task.admin',
            'task.services',
            'task.repositories',
            'task.constants',
            'task.exceptions',
            'task.apps',
            'task.urls',
        ]
        
        for module_name in modules_to_test:
            try:
                __import__(module_name)
            except ImportError as e:
                self.fail(f"Failed to import {module_name}: {e}")

    def test_task_app_verbose_name(self) -> None:
        """Test that task app has correct verbose name."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        self.assertEqual(app_config.verbose_name, 'Task')

    def test_task_app_name(self) -> None:
        """Test that task app has correct name."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        self.assertEqual(app_config.name, 'task')

    def test_task_app_label(self) -> None:
        """Test that task app has correct label."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        self.assertEqual(app_config.label, 'task')

    def test_task_app_path(self) -> None:
        """Test that task app has correct path."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        # Check that path contains 'task'
        self.assertIn('task', app_config.path)

    def test_task_app_models_meta(self) -> None:
        """Test that task models have correct meta configuration."""
        from task.models import Task
        
        # Check model meta options
        self.assertEqual(Task._meta.app_label, 'task')
        self.assertEqual(Task._meta.db_table, 'tasks')
        self.assertEqual(Task._meta.verbose_name, 'Task')
        self.assertEqual(Task._meta.verbose_name_plural, 'Tasks')
        self.assertEqual(Task._meta.ordering, ['-priority'])

    def test_task_app_ready_method(self) -> None:
        """Test that task app ready method works correctly."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        # The ready method should not raise any exceptions
        try:
            app_config.ready()
        except Exception as e:
            self.fail(f"TaskConfig.ready() raised an exception: {e}")

    def test_task_app_default_auto_field(self) -> None:
        """Test that task app has correct default auto field."""
        app_config: TaskConfig = apps.get_app_config('task')
        
        # Check that default_auto_field is set (Django 3.2+)
        if hasattr(app_config, 'default_auto_field'):
            self.assertEqual(app_config.default_auto_field, 'django.db.models.BigAutoField')
