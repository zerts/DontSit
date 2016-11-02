from datetime import datetime

from django import forms
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from post.models import Post
from .models import User

class NewPostForm(forms.Form):
    text = forms.CharField()
    TYPE = (
        (1, 'Plan'),
        (2, 'Achivement'),
        (3, 'Competition'),
    )
    type = forms.ChoiceField(
        choices=TYPE,
    )

#def addFriend(request, username):
    #if (request.method == 'POST'):


    #return redirect('/user/' + username)

def newPost(request):
    if (request.method == 'POST'):
        form = NewPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post(
                type=data['type'],
                text=data['text'],
                rating=0,
                time=datetime.now(),
                creator=request.user
            )
            post.save()

    else:
        form = NewPostForm()
    return redirect('/user/' + request.user.username)



class UserListView(ListView):
    model = User
    template_name = 'core/userList.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        users = User.objects.all()

        context['users'] = users
        return context

    '''def get_queryset(self):
        qs = super(UserListView, self).get_queryset()
        author = self.request.GET.get('author')
        if author:
            qs = qs.filter(username=author)
        return qs'''


class UserView(DetailView):
    model = User
    template_name = 'core/user.html'
    slug_field = 'username'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        currUser = User.objects.get(username=self.kwargs['slug'])

        form = NewPostForm()
        posts = Post.objects.filter(creator=currUser).order_by('-time')

        context['form'] = form
        context['posts'] = posts
        return context


# Create your views here.
