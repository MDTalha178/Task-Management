from rest_framework import status

from apps.users.models import User
from apps.users.serializer import GetUserSerializer, SignupSerializer
from apps.utils.utils import CustomModelView


class SignupViewSet(CustomModelView):
    """
    this class is used for signup viewlet where user can sign up
    """
    http_method_names = ('post',)
    serializer_class = SignupSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        """
        this method is used to create a signup data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = GetUserSerializer(user)
            return self.success_response(status_code=status.HTTP_201_CREATED, data=serializer.data)
        return self.failure_response(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
