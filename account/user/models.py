from django.db import models
# Create your models here.


class User(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    phone = models.IntegerField()
    email = models.EmailField(max_length=50)