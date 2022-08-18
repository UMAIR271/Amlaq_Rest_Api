from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.views import APIView
from loginapp.serializers import (UserRegistrationSerializer ,UserLoginSerializer, UserProfileSerializer, 
UserChangePasswordSerlizer, SendPasswordResetEmailSerlizer, UserPasswordResetSerializer,EmailVerificationSerializer,GoogleSocialAuthSerializer)
from django.contrib.auth import authenticate
from loginapp.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings

# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(GenericAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = UserRegistrationSerializer
    def post(self, request , format = None):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        user_data = serializer.data
        print(user_data)
        user = User.objects.get(email = user_data['email'])
        print(user)
        token = get_tokens_for_user(user)
        get_token = token['access']
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(get_token)
        email_body = 'Hi '+user.name + ' Use the link below to verify your email \n' + absurl
        data = {'body': email_body, 'to_email': user.email,'subject': 'Verify your email'}
        Util.send_email(data)
        return Response({"token":token, "mag": "Registraion success"}, status = status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])

    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = serializer.data.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY)
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_varified:
                user.is_varified = True
                user.save()
            return Response({'message':'Successfully activated','email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'message': 'Activation Expired','error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'message':'Invalid token', 'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        

class UserLoginView(GenericAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = UserLoginSerializer
    def post(self, request , format = None):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user =  authenticate(email=email, password=password)
        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"message":"Login Success","token":token,}, status=status.HTTP_200_OK)
        else:
            return Response({"message":'Email or Password is not Valid' ,"errors":{'none_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        


class UserProfileView(GenericAPIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    def get(self, request, format = None):
        serializer = self.serializer_class(request.user)
        print(serializer.data)
        return Response(serializer.data , status=status.HTTP_200_OK)



class UserChangePasswordView(GenericAPIView):

    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerlizer
    def post(self, request , format = None):
        serializer = self.serializer_class(data=request.data, context = {'user':request.user})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password changed Successfully"}, status=status.HTTP_200_OK)
        




class SendPasswordResetEmailView(GenericAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = SendPasswordResetEmailSerlizer
    def post(self , request , format= None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password Reset Link send . Please check your Email"},status=status.HTTP_200_OK)

class UserPasswordResetView(GenericAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = UserPasswordResetSerializer
    def post(self , request, uid, token, format= None):
        serializer = self.serializer_class(data=request.data , context ={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password Reset successfully"},status=status.HTTP_200_OK)
        
        


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
        