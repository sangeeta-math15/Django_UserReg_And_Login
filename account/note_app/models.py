from django.db import models

from user.models import User


class Notes(models.Model):
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=1200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
