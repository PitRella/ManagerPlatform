from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from project.models import Project

User = get_user_model()


class ProjectModelTest(TestCase):
    """Test cases for the Project model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )

    def test_project_creation(self):
        """Test that a project can be created."""
        assert self.project.title == 'Test Project'
        assert self.project.owner == self.user
        assert self.project.created_at is not None
        assert self.project.updated_at is not None

    def test_project_str_representation(self):
        """Test the string representation of a project."""
        expected_str = f"Test Project ({self.user.email})"
        assert str(self.project) == expected_str

    def test_unique_title_per_user_constraint(self):
        """Test that a user cannot have two projects with the same title."""
        with self.assertRaises(IntegrityError):
            Project.objects.create(
                title='Test Project',  # Same title as existing project
                owner=self.user  # Same owner
            )

    def test_project_manager_for_user(self):
        """Test the for_user method of ProjectManager."""
        # Create another project for the same user
        Project.objects.create(
            title='Another Project',
            owner=self.user
        )

        # Create a project for another user
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpassword'
        )
        Project.objects.create(
            title='Other User Project',
            owner=another_user
        )

        # Test that for_user returns only projects for the specified user
        user_projects = Project.objects.for_user(self.user)
        assert user_projects.count() == 2
        for project in user_projects:
            assert project.owner == self.user
