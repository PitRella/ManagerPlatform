from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from project.models import Project

User = get_user_model()


class ProjectUpdateViewTest(TestCase):
    """Test cases for the ProjectUpdateView."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.update_url = reverse('projects:update', kwargs={'pk': self.project.pk})

        # Create another user and their project
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpassword'
        )
        self.other_project = Project.objects.create(
            title='Other Project',
            owner=self.other_user
        )
        self.other_update_url = reverse('projects:update', kwargs={'pk': self.other_project.pk})

    def test_login_required(self):
        """Test that login is required to access the view."""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_get_update_form(self):
        """Test that GET request returns the update form."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/edit.html')
        self.assertContains(response, 'form')
        self.assertContains(response, self.project.title)

    def test_update_project_success(self):
        """Test that POST request with valid data updates a project."""
        self.client.login(username='testuser', password='testpassword')

        # Update the project
        response = self.client.post(
            self.update_url,
            data={'title': 'Updated Project Title'},
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )

        # Check response
        self.assertEqual(response.status_code, 200)

        # Check that the project was updated
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project Title')

        # Check that the response contains the updated title
        self.assertContains(response, 'Updated Project Title')

    def test_cannot_update_other_users_project(self):
        """Test that a user cannot update another user's project."""
        self.client.login(username='testuser', password='testpassword')

        # Try to update another user's project
        response = self.client.get(self.other_update_url)

        # Should return 404 Not Found
        self.assertEqual(response.status_code, 404)

        # Try to update via POST
        response = self.client.post(
            self.other_update_url,
            data={'title': 'Hacked Project'},
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )

        # Should return 404 Not Found
        self.assertEqual(response.status_code, 404)

        # Check that the other project was not updated
        self.other_project.refresh_from_db()
        self.assertEqual(self.other_project.title, 'Other Project')
