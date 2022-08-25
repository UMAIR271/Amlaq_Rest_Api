from django.urls import path, include
from .views import (UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView,VerifyOTP,
SendPasswordResetEmailView,UserPasswordResetView, VerifyEmail, GoogleSocialAuthView)

app_name = 'loginapp'

urlpatterns = [
    path('register/', UserRegistrationView.as_view() , name= "register"),
    path('VerifyOTP/', VerifyOTP.as_view() , name= "VerifyOTP"),
    path('email-verify/', VerifyEmail.as_view() , name= "email-verify"),
    path('login/', UserLoginView  .as_view() , name= "login"),
    path('profile/', UserProfileView.as_view() , name= "profile"),
    path('changepassword/', UserChangePasswordView.as_view() , name= "changepassword"),
    path('sendresetpasswordemail/', SendPasswordResetEmailView.as_view() , name= "sendresetpasswordemail"),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view() , name= "reset-password"),
    path('google/',  GoogleSocialAuthView.as_view() , name= "google"),





]