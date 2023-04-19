from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from core.settings import TWILIO_VERIFY_SERVICE, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
from .serializers import ChangePasswordSerializer, LoginSerializer, UserProfileSerializer, UserSerializer, VerificationSerializer, \
    VerificationCheckSerializer, LoginSerializer
from user.models import User


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class VerificationUser(GenericAPIView):
    serializer_class = VerificationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification = client.verify.services(TWILIO_VERIFY_SERVICE).verifications.create(
            to=serializer.data['phone_number'], channel='whatsapp')
        return Response({'is_pending': verification.status == 'pending'})
    

class VerificationCheck(GenericAPIView):
    serializer_class = VerificationCheckSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_check = client.verify.services(
        TWILIO_VERIFY_SERVICE).verification_checks.create(
            to=serializer.data['phone_number'], code=serializer.data['code'])
        return Response({'is_approved': verification_check.status == 'approved'})
     

class RegistrationAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0].key
        data = {'token': f'{token}'}
        data.update(serializer.data)
     
        return Response(data, status=201)


class LoginApi(GenericAPIView):
    
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = authenticate(phone_number=request.data['phone_number'], password=request.data['password'])
        if user:
            serializer = UserSerializer(user, many=False, context={'request': request})
            token = Token.objects.get_or_create(user=user)[0].key
            data = {'token': f'{token}',}
            profile = serializer.data
            data.update(profile)    
            return Response(data, status=200)
        return Response({'detail': 'Не существует пользователя или неверные данные'}, status=403)  


class ProfileApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, many=False)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=False)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(GenericAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, 
                data=request.data, partial=False, context={'request': request})  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
