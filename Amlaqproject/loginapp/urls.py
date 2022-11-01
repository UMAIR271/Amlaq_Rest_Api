from django.urls import path, include
from loginapp.views import *
app_name = 'loginapp'

urlpatterns = [
    path('register/', UserRegistrationView.as_view() , name= "register"),
    path('SendOtp/', SendOTP.as_view() , name= "SendOtp"),
    path('SendPhoneOtp/', send_phone_otp.as_view() , name= "SendPhoneOtp"),
    path('VerifyPhoneOTP/', VerifyPhoneOTP.as_view() , name= "VerifyPhoneOTP"),
    path('VerifyOTP/', VerifyOTP.as_view() , name= "VerifyOTP"),
    path('email-verify/', VerifyEmail.as_view() , name= "email-verify"),
    path('login/', UserLoginView  .as_view() , name= "login"),
    path('logout/', LogoutAPIView.as_view() , name= "logout"),
    path('profile/', UserProfileView.as_view() , name= "profile"),
    path('changepassword/', UserChangePasswordView.as_view() , name= "changepassword"),
    path('forgortpassword/', ChangePasswordView.as_view(), name='change-password'),
    path('google/',  GoogleSocialAuthView.as_view() , name= "google"),





]