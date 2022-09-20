from django.core.management.base import BaseCommand
from user.receive import Rabbitmq


class Command(BaseCommand):
    help = 'Register users'

    def handle(self, *args, **kwargs):
        Rabbitmq().run()
        self.stdout.write(self.style.SUCCESS('Success - A success.'))
        self.stdout.write(self.style.WARNING('warning - A warning.'))
