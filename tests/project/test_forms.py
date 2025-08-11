from django.test import TestCase
from django.contrib.auth import get_user_model

from project.forms import CreateForm, EditForm
from project.models import Project

User = get_user_model()


class CreateFormTest(TestCase):
    """Test cases for the CreateForm."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            title='Existing Project',
            owner=self.user
        )

    def test_valid_form(self):
        """Test that form is valid with correct data."""
        form_data = {'title': 'New Project'}
        form = CreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        """Test that form is invalid with empty title."""
        form_data = {'title': ''}
        form = CreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_whitespace_only_title(self):
        """Test that form is invalid with whitespace-only title."""
        form_data = {'title': '   '}
        form = CreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_title_too_long(self):
        """Test that form is invalid with title longer than 64 characters."""
        form_data = {'title': 'A' * 65}
        form = CreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_title_stripped(self):
        """Test that whitespace is stripped from title."""
        form_data = {'title': '  Test Title  '}
        form = CreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test Title')


class EditFormTest(TestCase):
    """Test cases for the EditForm."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            title='Existing Project',
            owner=self.user
        )

    def test_valid_form(self):
        """Test that form is valid with correct data."""
        form_data = {'title': 'Updated Project'}
        form = EditForm(data=form_data, instance=self.project)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        """Test that form is invalid with empty title."""
        form_data = {'title': ''}
        form = EditForm(data=form_data, instance=self.project)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_title_too_long(self):
        """Test that form is invalid with title longer than 64 characters."""
        form_data = {'title': 'A' * 65}
        form = EditForm(data=form_data, instance=self.project)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves correctly."""
        form_data = {'title': 'Updated Project'}
        form = EditForm(data=form_data, instance=self.project)
        self.assertTrue(form.is_valid())
        
        updated_project = form.save()
        self.assertEqual(updated_project.title, 'Updated Project')
        self.assertEqual(updated_project.id, self.project.id)