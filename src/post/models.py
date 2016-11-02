from __future__ import unicode_literals

from django.db import models

# Create your models here.
from core.models import User

class Note(models.Model):
    creator = models.ForeignKey(User, related_name='notes')
    text = models.CharField(max_length=1000, default='')
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(null=True)
    comments = models.ManyToManyField('Comment', blank=True)
    likes = models.ManyToManyField('Like', blank=True)

class Post(Note):
    type = models.IntegerField()

class Comment(Note):
    reply = models.ForeignKey(User, related_name='comments')

class Like(models.Model):
    creator = models.ForeignKey(User, related_name='likes')



