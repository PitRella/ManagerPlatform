from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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
        assert response.status_code == 302

    def test_get_create_form(self):
        """Test that GET request returns the create form."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.create_url)
        assert response.status_code == 200
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
        assert response.status_code == 200

        # Check that a project was created
        assert Project.objects.count() == initial_count + 1

        # Check project attributes
        project = Project.objects.latest('created_at')
        assert project.title == 'New Test Project'
        assert project.owner == self.user

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
        assert response.status_code == 422  # Unprocessable Entity

        # Check that no project was created
        assert Project.objects.count() == initial_count

        # Check that the response contains the form with errors
        assert 'form' in response.content.decode()
        assert 'error' in response.content.decode()

