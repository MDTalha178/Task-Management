from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.utils.models import TimestampedModel


class Task(TimestampedModel):
    """
     These models are used Create table or represents a table into my DB
    """
    name = models.CharField(_('task name'), max_length=255)
    description = models.TextField(_('task description'), blank=True)
    assigned_users = models.ManyToManyField(
        User,
        related_name='tasks',
        through='TaskAssignment',
        through_fields=['task', 'user']
    )
    priority = models.IntegerField(
        choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')],
        default=2
    )

    def __str__(self):
        return self.name


class TaskAssignment(TimestampedModel):
    """
    Separate model for task assignments with additional metadata
    Implements Composition over Inheritance
    """

    class TaskStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        REVIEW = 'review', _('Under Review')
        COMPLETED = 'completed', _('Completed')
        BLOCKED = 'blocked', _('Blocked')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_user_assignment_set')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_assignment_set')

    assigned_by = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )

    is_primary_assignee = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'task']
