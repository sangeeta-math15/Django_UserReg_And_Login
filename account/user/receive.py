import json
import pika
from django.conf import settings
from django.core.mail import send_mail
from .util import EncodeDecode


class Rabbitmq:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='send_mail')

    def send_email(self, data):
        payload = {"user_id": data.get('user_id'), "username": data.get('username')}
        token = EncodeDecode.encode_token(payload)
        # token = jwt.encode(payload, key=settings('SECRET_KEY', 'secret'), algorithm='HS256')
        send_mail(from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[data.get('user_email')],
                  message='Register yourself by complete this verification\n'
                          f'url is http://127.0.0.1:8000/user/verify_token/{token}',
                  subject='Link for the registration', )

    def callback(self, ch, method, properties, body):
        self.send_email(json.loads(body))
        print(" data =============== ", body)

    def run(self):
        self.channel.basic_consume(queue='send_mail', on_message_callback=self.callback, auto_ack=True)
        print("Started Consuming...")
        self.channel.start_consuming()
