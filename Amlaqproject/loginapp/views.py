from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from loginapp.serializers import (UserRegistrationSerializer ,UserLoginSerializer, UserProfileSerializer, 
UserChangePasswordSerlizer, SendPasswordResetEmailSerlizer, UserPasswordResetSerializer,EmailVerificationSerializer)
from django.contrib.auth import authenticate
from loginapp.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.urls import reverse
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

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request , format = None):
        print("hrlloooooo")
        serializer = UserRegistrationSerializer(data = request.data)
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


class VerifyEmail(APIView):
    renderer_classes = [UserRenderers]
    def get(self, request):
        try:
            serializer = EmailVerificationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = serializer.data.get('token')
            print("hello")
            payload = jwt.decode(token, settings.SECRET_KEY)
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_varified:
                user.is_varified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request , format = None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user =  authenticate(email=email, password=password)
        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"token":token, "mas":"Login Success"}, status=status.HTTP_200_OK)
        else:
            return Response({"errors":{'none_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        


class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data , status=status.HTTP_200_OK)



class UserChangePasswordView(APIView):

    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request , format = None):
        serializer = UserChangePasswordSerlizer(data=request.data, context = {'user':request.user})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password changed Successfully"}, status=status.HTTP_200_OK)
        




class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderers]
    def post(self , request , format= None):
        serializer = SendPasswordResetEmailSerlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password Reset Link send . Please check your Email"},status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    def post(self , request, uid, token, format= None):
        serializer = UserPasswordResetSerializer(data=request.data , context ={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password Reset successfully"},status=status.HTTP_200_OK)
        
        


        





