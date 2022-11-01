from django.core.mail import EmailMessage
import os 
import random
from loginapp.models import User
from django.conf import settings
from twilio.rest import Client


class Util:
    @staticmethod
    def send_email(data):
        otp = random.randint(1000,9999)
        email = EmailMessage(
            subject=data['subject'],
            body=f'Your otp is {otp}',
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()
        user_obj = User.objects.get(email=data['to_email'])
        user_obj.email_otp = otp
        user_obj.save()

    @staticmethod    
    def send_otp_to_phone(data):
        print("heloo")
        client = Client(os.environ.get('Account_SID'), os.environ.get('Auth_Token'))
        otp = random.randint(1000,9999)
        phone_number = data['phone_number']
        message = client.messages \
                        .create(
                            body=f"your otp is {otp}",
                            from_='+17078778695',
                            to=data['phone_number']
                        )
        print(message.sid)
        user_obj = User.objects.get(email=data['email'])
        user_obj.phone_number = phone_number
        user_obj.phone_otp = otp
        user_obj.save()


