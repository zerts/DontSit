import json

from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic import View

from core.models import User
from post.models import Post, Like

class EditPostForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea)
    TYPE = (
        (1, 'Plan'),
        (2, 'Achivement'),
        (3, 'Competition'),
    )
    type = forms.ChoiceField(
        choices=TYPE,
    )
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})


def editPost(request, pk):
    if (request.method == 'POST'):
        form = EditPostForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data
            curr_post = Post.objects.get(pk=pk)
            curr_post.type = data['type']
            curr_post.text = data['text']
            curr_post.save()
    return redirect(request.META.get('HTTP_REFERER'))

class PostView(DetailView):
    template_name = 'post/editPostForm.html'
    model = Post
    context_object_name = 'curr_post'


class PostLikes(View):

    def get(self, request):
        ids = request.GET.get('ids', '')
        ids = ids.split(',')
        posts = dict()
        for i in ids:
            posts[i] = [str(x.avatar) for x in list(
                User.objects.filter(
                    pk__in=Post.objects.get(pk=i).likes.all().values('creator'))
            )]
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
