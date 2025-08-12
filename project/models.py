from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins.models import TimestampMixin


class ProjectManager(models.Manager):  # type: ignore
    """
    Custom manager for a Project model providing user-specific queries.

    Extends the default Django model manager to add methods
    for filtering projects by user ownership.
    """

    def for_user(self, user) -> models.QuerySet:  # type: ignore
        """Returns projects for the given user."""
        return self.filter(owner=user)


class Project(TimestampMixin, models.Model):
    """
    Represents a project with a unique title per owner.

    Inherits from TimestampMixin to automatically manage creation and update.
    Each project is associated with an owner and
    enforces the uniqueness of the title per user.
    """

    title = models.CharField(
        max_length=64,
        verbose_name=_('Title'),
        help_text=_('Enter the name of the product'),
        unique=True,
        blank=False,
        null=False,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name=_('Owner'),
        help_text=_('Project owner'),
    )
    objects = ProjectManager()

    class Meta:
        db_table = 'projects'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'owner',
                    'title'
                ],
                name='unique_project_per_user'
            )
        ]

    def __str__(self) -> str:
        """Returns the project's title as its string representation."""
        return f"{self.title} ({self.owner.email})"
