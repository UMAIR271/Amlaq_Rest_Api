from django.core.mail import EmailMessage
import os 
import random
from loginapp.models import User


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
        user_obj.otp = otp
        user_obj.save()
        