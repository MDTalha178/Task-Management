"""
This file is used for urls or creating endpoint for API'S
"""
# Third party imports
from django.urls import path, include
from rest_framework import routers

from apps.users.views import SignupViewSet

# Local imports

router = routers.DefaultRouter()

router.register('signup', SignupViewSet, basename='signup')

urlpatterns = [
    path(r'auth/', include(router.urls)),
]