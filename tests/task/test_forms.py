from typing import TYPE_CHECKING
from django.test import TestCase
from django.contrib.auth import get_user_model

from task.forms import TaskForm
from project.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    User = AbstractUser
else:
    User = get_user_model()


class TaskFormTest(TestCase):
    """Test cases for TaskForm."""

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

    def test_task_form_valid_data(self) -> None:
        """Test form with valid data."""
        form_data: dict = {
            'text': 'Test task',
            'priority': 5
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['text'], 'Test task')
        self.assertEqual(form.cleaned_data['priority'], 5)

    def test_task_form_minimal_data(self) -> None:
        """Test form with minimal valid data."""
        form_data: dict = {
            'text': 'Test task'
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['text'], 'Test task')
        self.assertEqual(form.cleaned_data['priority'], 1)  # Default value

    def test_task_form_empty_text(self) -> None:
        """Test form with empty text."""
        form_data: dict = {
            'text': '',
            'priority': 1
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_task_form_whitespace_text(self) -> None:
        """Test form with whitespace-only text."""
        form_data: dict = {
            'text': '   ',
            'priority': 1
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_task_form_text_too_long(self) -> None:
        """Test form with text that's too long."""
        long_text: str = 'a' * 65  # More than max length of 64
        form_data: dict = {
            'text': long_text,
            'priority': 1
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_task_form_priority_too_low(self) -> None:
        """Test form with priority that's too low."""
        form_data: dict = {
            'text': 'Test task',
            'priority': 0
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)

    def test_task_form_priority_too_high(self) -> None:
        """Test form with priority that's too high."""
        form_data: dict = {
            'text': 'Test task',
            'priority': 1001
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)

    def test_task_form_priority_negative(self) -> None:
        """Test form with negative priority."""
        form_data: dict = {
            'text': 'Test task',
            'priority': -1
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)

    def test_task_form_priority_string(self) -> None:
        """Test form with priority as string."""
        form_data: dict = {
            'text': 'Test task',
            'priority': '5'
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['priority'], 5)

    def test_task_form_priority_invalid_string(self) -> None:
        """Test form with invalid priority string."""
        form_data: dict = {
            'text': 'Test task',
            'priority': 'invalid'
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)

    def test_task_form_boundary_values(self) -> None:
        """Test form with boundary values."""
        # Test minimum valid text length
        form_data: dict = {
            'text': 'a',  # Exactly 1 character
            'priority': 1
        }
        form: TaskForm = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test maximum valid text length
        form_data = {
            'text': 'a' * 64,  # Exactly 64 characters
            'priority': 1000
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test minimum valid priority
        form_data = {
            'text': 'Test task',
            'priority': 1
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test maximum valid priority
        form_data = {
            'text': 'Test task',
            'priority': 1000
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_save_method(self) -> None:
        """Test form save method."""
        form_data: dict = {
            'text': 'Test task',
            'priority': 5
        }
        form: TaskForm = TaskForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        
        # Test save without commit
        task = form.save(commit=False)
        self.assertEqual(task.text, 'Test task')
        self.assertEqual(task.priority, 5)
        self.assertFalse(task.completed)

    def test_task_form_fields_present(self) -> None:
        """Test that all expected fields are present in the form."""
        form: TaskForm = TaskForm()
        
        self.assertIn('text', form.fields)
        self.assertIn('priority', form.fields)

    def test_task_form_field_labels(self) -> None:
        """Test form field labels."""
        form: TaskForm = TaskForm()
        
        self.assertEqual(form.fields['text'].label, 'Text')
        self.assertEqual(form.fields['priority'].label, 'Priority')

    def test_task_form_field_help_text(self) -> None:
        """Test form field help text."""
        form: TaskForm = TaskForm()
        
        self.assertIn('Enter the task description', form.fields['text'].help_text)
        self.assertIn('Enter the task priority', form.fields['priority'].help_text)

    def test_task_form_field_max_length(self) -> None:
        """Test form field max length constraints."""
        form: TaskForm = TaskForm()
        
        self.assertEqual(form.fields['text'].max_length, 64)
        self.assertEqual(form.fields['priority'].max_value, 1000)
        self.assertEqual(form.fields['priority'].min_value, 1)
