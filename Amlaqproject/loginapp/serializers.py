from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from xml.dom import ValidationErr
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from loginapp.models import User
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} , write_only = True)
    class Meta :
        model = User
        fields = ['email', 'name', 'tc' , 'password', 'password2']
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






