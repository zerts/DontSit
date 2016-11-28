import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from core.models import User
from post.models import Post, Like


class PostLikes(View):

    def get(self, request):
        ids = request.GET.get('ids', '')
        ids = ids.split(',')
        posts = dict()
        for i in ids:
            posts[i] = [x.username for x in list(
                User.objects.filter(
                    pk__in=Post.objects.get(pk=i).likes.all().values('creator')))]
        return HttpResponse(json.dumps(posts))

class PostLikesView(View):
    curr_post = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.curr_post = get_object_or_404(Post, pk=pk)
        return super(PostLikesView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        returnList = self.curr_post.likes.all().values_list('creator')
        return HttpResponse(returnList)

    def post(self, request):
        if not(request.user.username in [x.username for x in list(
                User.objects.filter(
                    pk__in=self.curr_post.likes.all().values('creator')))]):
            newLike = Like(creator=User.objects.get(username=request.user.username))
            newLike.save()
            self.curr_post.likes.add(newLike)
            self.curr_post.save()
        else:
            self.curr_post.likes.remove(
                *self.curr_post.likes.filter(
                    creator__username=request.user.username))
            self.curr_post.save()
        return HttpResponse(self.curr_post.likes)
# Create your views here.
