from rest_framework import status
from rest_framework.decorators import action

from apps.tasks.manager.task_manager import TaskService
from apps.tasks.models import Task
from apps.tasks.serializer import TaskSerializer, GetTaskSerializer, AssignTaskSerializer
from apps.users.models import User
from apps.utils.messages import CustomError
from apps.utils.utils import CustomModelView


class TaskViewSet(CustomModelView):
    """
    this class is used for signup viewlet where user can sign up
    """
    http_method_names = ('post', 'get',)
    serializer_class = TaskSerializer
    queryset = TaskService

    def create(self, request, *args, **kwargs):
        """
        this method is used to create a signup data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            serializer = GetTaskSerializer(serializer)
            return self.success_response(status_code=status.HTTP_201_CREATED, data=serializer.data)
        return self.failure_response(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @action(methods=['POST'], detail=False, url_name='assign-task', url_path='assign-task',
            serializer_class=AssignTaskSerializer)
    def assign_task(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            serializer = TaskSerializer(serializer)
            return self.success_response(status_code=status.HTTP_201_CREATED, data=serializer.data)
        return self.failure_response(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @action(methods=['GET'], detail=False, url_name='user-task', url_path='user-task',
            serializer_class=GetTaskSerializer)
    def get_user_task(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user', None)
        user_id = '6'
        if user_id is None:
            return self.failure_response(
                status_code=status.HTTP_400_BAD_REQUEST, data=CustomError.get_error_message('USER_ID_REQUIRED')
            )
        user = User.objects.get(id=user_id)
        serializer = self.serializer_class(
            TaskService.get_user_tasks(user), context={'user_id': user_id}, many=True
        )
        return self.success_response(status_code=status.HTTP_200_OK, data=serializer.data)
