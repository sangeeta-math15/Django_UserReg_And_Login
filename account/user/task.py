from celery import shared_task
from django.core.mail import send_mail

from account import settings
from user.util import EncodeDecode


@shared_task()
def send_email_task(userid, to, username):
    token = EncodeDecode.encode_token({"user_id": userid, "username": username})

    send_mail(from_email=settings.EMAIL_HOST_USER,
              recipient_list=[to],
              message='Register yourself by complete this verification'
                      f'url is http://127.0.0.1:8000/user/verify_token/{token}',
              subject='Link for the registration', )
