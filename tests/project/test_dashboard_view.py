from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from project.models import Project

User = get_user_model()


class DashboardViewTest(TestCase):
    """Test cases for the DashboardView."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.dashboard_url = reverse('projects:dashboard')

        # Create some projects for the user
        self.projects = []
        for i in range(15):  # Create 15 projects to test pagination
            project = Project.objects.create(
                title=f'Test Project {i}',
                owner=self.user
            )
            self.projects.append(project)

        # Create another user and their project
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpassword'
        )
        self.other_project = Project.objects.create(
            title='Other User Project',
            owner=self.other_user
        )

    def test_login_required(self):
        """Test that login is required to access the view."""
        response = self.client.get(self.dashboard_url)
        assert response.status_code == 302

    def test_dashboard_displays_user_projects(self):
        """Test that dashboard displays only the current user's projects."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.dashboard_url)

        assert response.status_code == 200
        self.assertTemplateUsed(response, 'project/dashboard.html')

        # Check that the response does not contain the other user's project
        self.assertNotContains(response, self.other_project.title)

    def test_dashboard_pagination(self):
        """Test that dashboard paginates projects correctly."""
        self.client.login(username='testuser', password='testpassword')

        # First page
        response = self.client.get(self.dashboard_url)
        assert response.status_code == 200
        assert len(response.context['projects']) == 10

        # Second page
        response = self.client.get(f'{self.dashboard_url}?page=2')
        assert response.status_code == 200
        assert len(response.context['projects']) == 5

    def test_empty_dashboard(self):
        """Test that dashboard handles case with no projects."""
        # Create a new user with no projects
        User.objects.create_user(
            username='emptyuser',
            email='empty@example.com',
            password='testpassword'
        )

        self.client.login(username='emptyuser', password='testpassword')
        response = self.client.get(self.dashboard_url)
        assert response.status_code == 200
        assert len(response.context['projects']) == 0

        # Check that the projects container exists but is empty
        assert '<div id="projects-container">' in response
        assert 'class="todo-list-project"' in response
