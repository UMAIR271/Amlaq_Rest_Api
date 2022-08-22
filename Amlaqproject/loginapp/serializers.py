from dataclasses import fields
from pyexpat import model
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from xml.dom import ValidationErr
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .register import register_social_user
from rest_framework import serializers
from . import google
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from loginapp.models import User
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} , write_only = True)
    class Meta :
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only' : True
            }
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confrim Password doesn't match")
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class SendOtpSerializers(serializers.Serializer):
    email = serializers.EmailField()


class VerifyAccountSerializers(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']


class UserChangePasswordSerlizer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    class Meta:
        fields = ['password','password2']


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confrim Password doesn't match")
        user.set_password(password)
        user.save()
        return data



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['password','password2']


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confrim Password doesn't match")
        user.set_password(password)
        user.save()
        return data


class SendPasswordResetEmailSerlizer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/'+ uid + "/" + token
            body = 'Click Following Link to Reset Your Password'+" " + link
            data = {
                "subject":"Reset your Password",
                "body":body,
                "to_email": user.email

            }
            Util.send_email(data)
            
            return data  
        else:
            raise ValidationErr("You are not Register User")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style= {'input_type':'password'}, write_only = True)
    class Meta:
        fields = ['password','password2']


    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token') 
            if password != password2:
                raise serializers.ValidationError("Password and Confrim Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr("token is not valid or Expied")
            user.set_password(password)
            user.save()
            return data

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr("token is not valid or Expied")



# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('old_password', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value

#     def update(self, instance, validated_data):

#         instance.set_password(validated_data['password'])
#         instance.save()

#         return instance



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)




