from rest_framework import serializers
from apps.tasks.models import Task, TaskAssignment
from apps.users.models import User
from apps.tasks.manager.task_manager import TaskService
from apps.users.serializer import GetUserSerializer


class TaskAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Task Assignments with Nested Information
    """
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ['user', 'user_name', 'is_primary_assignee', 'status']


class TaskSerializer(serializers.ModelSerializer):
    """
    Comprehensive Task Serializer with Advanced Validations
    """
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )
    assignments = TaskAssignmentSerializer(
        source='taskassignment_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description',
            'priority', 'assigned_users',
            'assignments',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """
        Custom create method to handle user assignments
        """
        assigned_users = validated_data.pop('assigned_users', [])
        task = TaskService.create_task(
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            assigned_users=assigned_users
        )
        return task


class AssignTaskSerializer(serializers.ModelSerializer):
    """
    this serializer class is used to assign a task
    """
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.filter(),
        required=False, allow_null=False
    )
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'task', 'assigned_users',
        ]

    def create(self, validated_data):
        """
        Custom create method to handle user assignments
        """
        assigned_users = validated_data.pop('assigned_users', [])
        task = TaskService.assign_task_to_users(
            task=validated_data['task'],
            users=assigned_users,
        )
        task = validated_data.get('task')
        return task


class GetTaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = ('id', 'status', 'completed_at', 'is_primary_assignee',)


class GetTaskSerializer(serializers.ModelSerializer):
    task_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_user_details(self, obj):
        """
        Fetch task assignments only for the given user_id
        """
        user_id = self.context.get('user_id')
        if user_id:
            user_obj = obj.task_assignment_set.filter(user_id=user_id).first().user
            return GetUserSerializer(user_obj, many=False).data
        return None

    def get_task_details(self, obj):
        """
        Fetch task assignments only for the given user_id
        """
        user_id = self.context.get('user_id')
        if user_id:
            task_assignments = obj.task_assignment_set.filter(user_id=user_id)
            return GetTaskAssignmentSerializer(task_assignments, many=True).data
        return None

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description',
            'priority', 'user_details', 'task_details',
        ]
