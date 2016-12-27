from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    friends = models.ManyToManyField('self')



class Achievment(models.Model):
    avatar = models.ImageField(null=True)
    type = models.IntegerField(default=0)

