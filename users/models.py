from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, blank=True, validators=[UnicodeUsernameValidator()])
    avatar = models.ImageField(max_length=255, blank=True, upload_to='avatars/')

    def __str__(self):
        return f'{self.username}'
