from django.db import transaction
from apps.tasks.models import Task, TaskAssignment


class TaskService:
    """
    This class is responsible to Create task and assign a task
    """

    @classmethod
    @transaction.atomic
    def create_task(cls, name, description, assigned_users=None):
        """
        Create a task with optional user assignments
        Implements Transaction and Validation
        """
        task = Task.objects.create(
            name=name,
            description=description,
        )

        if assigned_users:
            cls.assign_task_to_users(task, assigned_users)
        return task

    @classmethod
    @transaction.atomic
    def assign_task_to_users(cls, task, users, assigned_by=None):
        """
        Assign task to multiple users with validation
        """
        assignments = []
        for index, user in enumerate(users):
            assignment = TaskAssignment.objects.create(
                task=task,
                user=user,
                assigned_by=assigned_by,
                is_primary_assignee=(index == 0)
            )
            assignments.append(assignment)

        return assignments

    @classmethod
    def get_user_tasks(cls, user, status=None):
        """
        Retrieve tasks for a specific user with optional filtering
        """
        tasks = user.tasks.all()
        if status:
            tasks = tasks.filter(status=status)

        return tasks
