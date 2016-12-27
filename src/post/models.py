from __future__ import unicode_literals

from django.db import models

# Create your models here.
from core.models import User

class PostQuerySet(models.QuerySet):

    def show_my(self, user):
        return self.filter(models.Q(creator=user)).order_by('-time')

class Like(models.Model):
    creator = models.ForeignKey(User, related_name='likes')

class Note(models.Model):
    creator = models.ForeignKey(User, related_name='notes')
    text = models.CharField(max_length=1000, default='')
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(null=True)
    likes = models.ManyToManyField(Like)



class Comment(Note):
    reply = models.ForeignKey(User, related_name='comments')

class Post(Note):
    type = models.IntegerField()
    comments = models.ManyToManyField(Comment)

    objects = PostQuerySet.as_manager()


