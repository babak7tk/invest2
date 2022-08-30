import requests
from django.conf import settings


def send_sms(receiver, msg):
    try:
        response = requests.get(
        f'{settings.SMS_WEBSERVICE_URL}&From={settings.SMS_SENDER_NUMBER}&Text={msg}&To={receiver}'
    )
    except:
        return False
    response = response.json()

    if response.get('ResultStatusCode') != 1 and not response.get('Data'):
        return False
    return True
