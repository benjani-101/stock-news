from twilio.rest import Client
from config import TW_PHONE_NUMBER


def sms_message(account_sid, auth_token, message, to_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                  body=message,
                                  from_=TW_PHONE_NUMBER,
                                  to=to_number
                              )

    print(message.sid)
    print(message.status)