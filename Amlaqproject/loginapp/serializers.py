
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from xml.dom import ValidationErr
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .register import register_social_user
from listing.serializers import getListingSerializer
from rest_framework import serializers
from . import google
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from loginapp.models import User
from .utils import Util
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} , write_only = True)
    class Meta :
        model = User
        fields = ['email', 'username', 'password', 'password2', "profile_image"]
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

    def create(self, validate_data, **extra_fields):
        return User.objects.create_user(**validate_data, **extra_fields)

class SendOtpSerializers(serializers.Serializer):
    email = serializers.EmailField()

# class SendPhoneOtpSerializers(serializers.Serializer):
#     email = serializers.EmailField()
#     phone_number = serializers.CharField()

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
    # profile_image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ('email','password')
    
    def get_image_url(self, obj):
        return obj.profile_image.url


# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length = 255)
#     class Meta:
#         model = User
#         fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    # image_url = serializers.ImageField(source="profile_image", read_only=True)
    # userdata = UserRegistrationSerializer(many=True, read_only=True)
    # listingdata = getListingSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email','username','email_varified','is_active','created_at','updated_at','auth_provider','profile_image',  'photo_url']
    def get_photo_url(self, User):
        request = self.context.get('request')
        photo_url = User.profile_image.url
        return request.build_absolute_uri(photo_url)

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
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

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
        username = user_data['username']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, usermname=username)


