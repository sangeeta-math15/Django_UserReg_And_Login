from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    this class created for adding the table in database
    """
    phone = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
            ),
        ],
    )
    is_verified = models.BooleanField(default=False)


class UserLogs(models.Model):
    request_method = models.CharField(max_length=50)
    request_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=False,blank=False)
