from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from .api import *

urlpatterns = [
	path('swagger/', get_swagger_view(title='API')),
	path('cafe/', CafeViewSet),
	path('items/', ItemViewSet),
	path('categories/', CategoryViewSet),
]
