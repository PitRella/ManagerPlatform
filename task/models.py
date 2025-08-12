from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    text = models.CharField(
        max_length=64,
        verbose_name=_('Text'),
        help_text=_('Enter the task description'),
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'),
        help_text=_('Enter the task priority'),
        default=1
    )
    completed = models.BooleanField(
        verbose_name=_('Completed'),
        help_text=_('Check if the task is completed'),
        default=False
    )
    project = models.ForeignKey(
        'project.Project',
        verbose_name=_('Project'),
        help_text=_('Select the project'),
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-priority']

    def __str__(self) -> str:
        return self.text
