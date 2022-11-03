from django.db import models
from user.models import User


class Labels(models.Model):
    title = models.CharField(max_length=400)
    color = models.CharField(max_length=50)
    font = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Notes(models.Model):
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=1200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    labels = models.ManyToManyField(Labels, related_name='labels')
