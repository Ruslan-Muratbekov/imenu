from django.urls import path
from .views import ChangePasswordView, ProfileApiView, RegistrationAPIView
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from .views import VerificationUser, VerificationCheck, LoginApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    #path('login/', TokenObtainPairView.as_view(
    #    serializer_class = CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('profile', ProfileApiView.as_view()),
    path('login/', LoginApi.as_view()),
    path('registretion/', RegistrationAPIView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    #path('login/refresh/', TokenRefreshView.as_view(
    #    serializer_class=CustomTokenRefreshSerializer), name='token_refresh'),
    #path('login/verify_token/', TokenVerifyView.as_view(), name='token_verify'),
    path('verify_by_whatsapp/', VerificationUser.as_view()),
    path('verify_by_whatsapp/check/', VerificationCheck.as_view()),
]