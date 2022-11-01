from django.conf import settings
from twilio.rest import Client
import random
from loginapp.models import User


class MessageHandler:
    phone_number = None
    otp = None
    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number
        self.otp = random.randint(1000,9999)

    def send_otp_to_phone(self):
        client = Client(settings.account_sid,settings.auth_token)

        message = client.messages \
                        .create(
                            body=f"your otp is {self.otp}",
                            from_='+17078778695',
                            to=self.phone_number
                        )
        user_obj = User.objects.get(email=data['to_email'])
        

        print(message.sid)
