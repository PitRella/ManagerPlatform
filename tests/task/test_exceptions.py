from typing import TYPE_CHECKING
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from task.exceptions import (
    TaskNotFoundError,
    TaskPermissionError,
    ProjectNotFoundError,
    TaskValidationError,
    TaskReorderError,
    TaskToggleError
)
from task.models import Task
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskExceptionsTest(TestCase):
    """Test cases for Task exceptions."""

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
        self.task: Task = Task.objects.create(
            text='Test task',
            project=self.project,
            priority=1
        )

    def test_task_not_found_error(self) -> None:
        """Test TaskNotFoundError exception."""
        error: TaskNotFoundError = TaskNotFoundError("Task not found")
        
        self.assertEqual(str(error), "Task not found")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, TaskNotFoundError)

    def test_task_permission_error(self) -> None:
        """Test TaskPermissionError exception."""
        error: TaskPermissionError = TaskPermissionError("Permission denied")
        
        self.assertEqual(str(error), "Permission denied")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, TaskPermissionError)

    def test_project_not_found_error(self) -> None:
        """Test ProjectNotFoundError exception."""
        error: ProjectNotFoundError = ProjectNotFoundError("Project not found")
        
        self.assertEqual(str(error), "Project not found")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, ProjectNotFoundError)

    def test_task_validation_error(self) -> None:
        """Test TaskValidationError exception."""
        error: TaskValidationError = TaskValidationError("Validation failed")
        
        self.assertEqual(str(error), "Validation failed")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, TaskValidationError)

    def test_task_reorder_error(self) -> None:
        """Test TaskReorderError exception."""
        error: TaskReorderError = TaskReorderError("Reorder failed")
        
        self.assertEqual(str(error), "Reorder failed")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, TaskReorderError)

    def test_task_toggle_error(self) -> None:
        """Test TaskToggleError exception."""
        error: TaskToggleError = TaskToggleError("Toggle failed")
        
        self.assertEqual(str(error), "Toggle failed")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, TaskToggleError)

    def test_exception_inheritance(self) -> None:
        """Test that all task exceptions inherit from appropriate base classes."""
        exceptions: list = [
            TaskNotFoundError("test"),
            TaskPermissionError("test"),
            ProjectNotFoundError("test"),
            TaskValidationError("test"),
            TaskReorderError("test"),
            TaskToggleError("test")
        ]
        
        for exception in exceptions:
            self.assertIsInstance(exception, Exception)
            self.assertIsInstance(exception, (TaskNotFoundError, TaskPermissionError, 
                                            ProjectNotFoundError, TaskValidationError,
                                            TaskReorderError, TaskToggleError))

    def test_exception_with_custom_message(self) -> None:
        """Test exceptions with custom error messages."""
        custom_message: str = "Custom error message for task operations"
        
        task_not_found: TaskNotFoundError = TaskNotFoundError(custom_message)
        task_permission: TaskPermissionError = TaskPermissionError(custom_message)
        project_not_found: ProjectNotFoundError = ProjectNotFoundError(custom_message)
        task_validation: TaskValidationError = TaskValidationError(custom_message)
        task_reorder: TaskReorderError = TaskReorderError(custom_message)
        task_toggle: TaskToggleError = TaskToggleError(custom_message)
        
        self.assertEqual(str(task_not_found), custom_message)
        self.assertEqual(str(task_permission), custom_message)
        self.assertEqual(str(project_not_found), custom_message)
        self.assertEqual(str(task_validation), custom_message)
        self.assertEqual(str(task_reorder), custom_message)
        self.assertEqual(str(task_toggle), custom_message)

    def test_exception_with_empty_message(self) -> None:
        """Test exceptions with empty messages."""
        empty_message: str = ""
        
        task_not_found: TaskNotFoundError = TaskNotFoundError(empty_message)
        task_permission: TaskPermissionError = TaskPermissionError(empty_message)
        project_not_found: ProjectNotFoundError = ProjectNotFoundError(empty_message)
        task_validation: TaskValidationError = TaskValidationError(empty_message)
        task_reorder: TaskReorderError = TaskReorderError(empty_message)
        task_toggle: TaskToggleError = TaskToggleError(empty_message)
        
        self.assertEqual(str(task_not_found), empty_message)
        self.assertEqual(str(task_permission), empty_message)
        self.assertEqual(str(project_not_found), empty_message)
        self.assertEqual(str(task_validation), empty_message)
        self.assertEqual(str(task_reorder), empty_message)
        self.assertEqual(str(task_toggle), empty_message)

    def test_exception_with_none_message(self) -> None:
        """Test exceptions with None messages."""
        none_message: None = None
        
        task_not_found: TaskNotFoundError = TaskNotFoundError(none_message)
        task_permission: TaskPermissionError = TaskPermissionError(none_message)
        project_not_found: ProjectNotFoundError = ProjectNotFoundError(none_message)
        task_validation: TaskValidationError = TaskValidationError(none_message)
        task_reorder: TaskReorderError = TaskReorderError(none_message)
        task_toggle: TaskToggleError = TaskToggleError(none_message)
        
        self.assertEqual(str(task_not_found), "None")
        self.assertEqual(str(task_permission), "None")
        self.assertEqual(str(project_not_found), "None")
        self.assertEqual(str(task_validation), "None")
        self.assertEqual(str(task_reorder), "None")
        self.assertEqual(str(task_toggle), "None")

    def test_exception_equality(self) -> None:
        """Test exception equality."""
        error1: TaskNotFoundError = TaskNotFoundError("Same message")
        error2: TaskNotFoundError = TaskNotFoundError("Same message")
        error3: TaskNotFoundError = TaskNotFoundError("Different message")
        
        # Same type and message should be equal
        self.assertEqual(error1.args, error2.args)
        self.assertEqual(str(error1), str(error2))
        
        # Different messages should not be equal
        self.assertNotEqual(error1.args, error3.args)
        self.assertNotEqual(str(error1), str(error3))

    def test_exception_different_types(self) -> None:
        """Test that different exception types are not equal."""
        task_not_found: TaskNotFoundError = TaskNotFoundError("Same message")
        task_permission: TaskPermissionError = TaskPermissionError("Same message")
        
        # Different types should not be equal even with same message
        self.assertNotEqual(type(task_not_found), type(task_permission))
        self.assertNotEqual(task_not_found.__class__, task_permission.__class__)

    def test_exception_attributes(self) -> None:
        """Test exception attributes."""
        message: str = "Test error message"
        error: TaskNotFoundError = TaskNotFoundError(message)
        
        self.assertEqual(error.args[0], message)
        self.assertEqual(len(error.args), 1)
        self.assertIn(message, error.args)

    def test_exception_multiple_arguments(self) -> None:
        """Test exceptions with multiple arguments."""
        error: TaskNotFoundError = TaskNotFoundError("Task", "not", "found")
        
        self.assertEqual(len(error.args), 3)
        self.assertEqual(error.args[0], "Task")
        self.assertEqual(error.args[1], "not")
        self.assertEqual(error.args[2], "found")
        self.assertEqual(str(error), "('Task', 'not', 'found')")
