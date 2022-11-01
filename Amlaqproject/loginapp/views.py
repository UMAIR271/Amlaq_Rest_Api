from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from loginapp.serializers import *
from django.contrib.auth import authenticate
from loginapp.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
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

class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderers]
    serializer_class = UserRegistrationSerializer
    def post(self, request , format = None):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                user_data = serializer.data
                user = User.objects.get(email = user_data['email'])
                data = User.objects.filter(email = user_data['email']).values(
                    'id', 'email','username','email_varified','is_active','created_at','updated_at','auth_provider', 'profile_image')
                print(data)
                token = get_tokens_for_user(user)
                # data = {'to_email': user.email,'subject': 'Verify your email'}
                # Util.send_email(data)
                return Response({ "message": "Registraion success","token":token['access'],"user_obj":data}, status = status.HTTP_200_OK)
            
            for key, values in serializer.errors.items():
                error = [value[:] for value in values]
                print(error)
            
            return Response({ "message": error, 'error': serializer.errors }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as e:
            print(e)
            print(type(e))
            return Response({'error': e }, status = status.HTTP_404_NOT_FOUND)


class SendOTP(APIView):

    def post(self, request):
        try:
            data = request.data 
            serializer =  SendOtpSerializers(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                print(email)
                user = User.objects.get(email = email)
                print(user)
                if not user:
                    return Response({ "message": "invalid Email", 'error': "invalid Email" }, status = status.HTTP_401_UNAUTHORIZED)

                data = {'to_email': user.email,'subject': 'Verify your email'}
                Util.send_email(data)
                return Response({ "message": "Please Check your email"}, status = status.HTTP_200_OK)
            
            for key, values in serializer.errors.items():
                error = [value[:] for value in values]
                var=error[0].replace('This', key)
                print(var)
                return Response({ "message": var, 'error': serializer.errors }, status = status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(e)
            print(type(e))
            return Response({'error': serializer.errors }, status = status.HTTP_404_NOT_FOUND)


class VerifyOTP(APIView):

    def post(self, request):
        try:
            data = request.data 
            serializer =  VerifyAccountSerializers(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.filter(email = email)
                print(user)
                if not user.exists():
                    return Response({ "message": "invalid Email", 'error': "invalid Email" }, status = status.HTTP_401_UNAUTHORIZED)
                print(otp)
                if user[0].email_otp != otp:
                    return Response({ "message": "OTP is Wrong", 'error': "OTP is Wrong" }, status = status.HTTP_401_UNAUTHORIZED)
                user = user.first()
                user.email_varified = True
                user.save()
                return Response({ "message": "Account verified","data":"Account verified",}, status = status.HTTP_201_CREATED)
            
            for key, values in serializer.errors.items():
                error = [value[:] for value in values]
                var=error[0].replace('This', key)
                print(var)
                return Response({ "message": var, 'error': serializer.errors }, status = status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({'error': str(e) }, status = status.HTTP_404_NOT_FOUND)
            


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
    # renderer_classes = [UserRenderers]
    serializer_class = UserLoginSerializer
    def post(self, request , format = None):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user =  authenticate(email=email, password=password)
        print(user)
        if user is not None:
            user_object = User.objects.filter(email = email).values(
                    'id', 'email','username','email_varified','is_active','created_at','updated_at','auth_provider','profile_image')
            token = get_tokens_for_user(user)
            return Response({"message":"Login Success","token":token,"user_object":user_object}, status=status.HTTP_200_OK)
        else:
            return Response({"message":'Email or Password is not Valid' ,"errors":{'none_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        
        
        


class UserProfileView(APIView):
    # renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, format = None):
        serializer = self.serializer_class(request.user , context={"request": request})
        data = serializer.data
        email = data['email']
        user = User.objects.get(email = email)
        if not user:
                    return Response({ "message": "invalid Email", 'error': "invalid Email" }, status = status.HTTP_401_UNAUTHORIZED)
        user_object = User.objects.filter(email = email).values(
                    'id', 'email','username','email_varified','is_active','created_at','updated_at','auth_provider', 'phone_number')
        return Response({'data':data ,'user_object':user_object}, status=status.HTTP_200_OK)




class UserChangePasswordView(GenericAPIView):

    renderer_classes = [UserRenderers]
    # permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerlizer
    def post(self, request , format = None):
        data=request.data
        user = request.user
        email= data['email']
        user = User.objects.get(email = email)
        serializer = self.serializer_class(data=request.data, context = {'user':user})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        return Response({"mas":"Password changed Successfully"}, status=status.HTTP_200_OK)
        


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token = get_tokens_for_user(user)
        # token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token['access']}, status=status.HTTP_200_OK)




class send_phone_otp(APIView):
    def post(self, request):
        data = request.data 
        print(data)
        # serializer =  SendOtpSerializers(data=data)
        # if serializer.is_valid():
        if data.get('phone_number') is None:
            return Response(
                {"message":"please enter the phone_number"},
                status=status.HTTP_400_BAD_REQUEST
            )  
        if User.objects.filter(phone_number=data.get('phone_number')).exists():
            return Response(
                {"message":"The phone_number is already exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if data.get('email') is None:
            return Response(
                {"message":"please enter the email"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data =  {
            'email': data.get('email'),
            'phone_number': data.get('phone_number')
            } 
        print("pak")   
        Util.send_otp_to_phone(data)
        return Response({ "message": "Please Check your Phone"}, status = status.HTTP_200_OK)

class VerifyPhoneOTP(APIView):

    def post(self, request):
        try:
            print("enter")
            data = request.data 
            phone_number = data.get('phone_number')
            otp = data.get('otp')
            user = User.objects.filter(phone_number = phone_number)
            print(user)
            if not user.exists():
                return Response({ "message": "invalid phone_number", 'error': "invalid phone_number" }, status = status.HTTP_401_UNAUTHORIZED)
            if user[0].phone_otp != otp:
                return Response({ "message": "OTP is Wrong", 'error': "OTP is Wrong" }, status = status.HTTP_401_UNAUTHORIZED)
            user = user.first()
            user.phone_varified = True
            user.save()
            return Response({ "message": "Phone_number verified","data":"Phone_number verified",}, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': e }, status = status.HTTP_404_NOT_FOUND)

class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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