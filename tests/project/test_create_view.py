from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from project.models import Project

User = get_user_model()


class ProjectCreateViewTest(TestCase):
    """Test cases for the ProjectCreateView."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.create_url = reverse('projects:create')

    def test_login_required(self):
        """Test that login is required to access the view."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_get_create_form(self):
        """Test that GET request returns the create form."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/create.html')
        self.assertContains(response, 'form')

    def test_create_project_success(self):
        """Test that POST request with valid data creates a project."""
        self.client.login(username='testuser', password='testpassword')

        # Initial count
        initial_count = Project.objects.count()

        # Create a project
        response = self.client.post(
            self.create_url,
            data={'title': 'New Test Project'},
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )

        # Check response
        self.assertEqual(response.status_code, 200)

        # Check that a project was created
        self.assertEqual(Project.objects.count(), initial_count + 1)

        # Check project attributes
        project = Project.objects.latest('created_at')
        self.assertEqual(project.title, 'New Test Project')
        self.assertEqual(project.owner, self.user)

    def test_create_project_invalid_data(self):
        """Test that POST request with invalid data returns form with errors."""
        self.client.login(username='testuser', password='testpassword')

        # Initial count
        initial_count = Project.objects.count()

        # Try to create a project with empty title
        response = self.client.post(
            self.create_url,
            data={'title': ''},
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )

        # Check response
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

        # Check that no project was created
        self.assertEqual(Project.objects.count(), initial_count)

        # Check that the response contains the form with errors
        self.assertContains(response, 'form', status_code=422)
        self.assertContains(response, 'error', status_code=422)

    def test_create_project_duplicate_title(self):
        """Test that creating a project with a duplicate title fails."""
        self.client.login(username='testuser', password='testpassword')

        # Create a project first
        Project.objects.create(
            title='Duplicate Title',
            owner=self.user
        )

        # Initial count
        initial_count = Project.objects.count()

        # Try to create another project with the same title
        response = self.client.post(
            self.create_url,
            data={'title': 'Duplicate Title'},
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )

        # Check response
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

        # Check that no new project was created
        self.assertEqual(Project.objects.count(), initial_count)
