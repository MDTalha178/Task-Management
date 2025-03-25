"""
This file is used for urls or creating endpoint for API'S
"""
# Third party imports
from django.urls import path, include
from rest_framework import routers

from apps.tasks.views import TaskViewSet

# Local imports

router = routers.DefaultRouter()

router.register('task', TaskViewSet, basename='task')

urlpatterns = [
    path(r'', include(router.urls)),
]