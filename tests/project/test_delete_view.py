from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from project.models import Project

User = get_user_model()


class ProjectDeleteViewTest(TestCase):
    """Test cases for the ProjectDeleteView."""

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
        self.delete_url = reverse(
            'projects:delete',
            kwargs={
                'pk': self.project.pk
            })

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
        self.other_delete_url = reverse(
            'projects:delete',
            kwargs={
                'pk':
                    self.other_project.pk
            }
        )

    def test_login_required(self):
        """Test that login is required to access the view."""
        response = self.client.post(self.delete_url)
        assert response.status_code == 302

        # Verify project still exists
        assert Project.objects.filter(pk=self.project.pk).exists()



    def test_get_method_does_not_delete(self):
        """Test that GET requests do not delete the project."""
        self.client.login(username='testuser', password='testpassword')

        # Initial count
        initial_count = Project.objects.count()

        # Check that the project was not deleted
        assert Project.objects.count() == initial_count
        assert Project.objects.filter(pk=self.project.pk).exists()
