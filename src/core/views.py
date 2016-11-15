from datetime import datetime
from itertools import chain
from operator import attrgetter

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView, ListView

from post.models import Post
from .models import User

class NewPostForm(forms.Form):

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
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})

def newPost(request):
    if (request.method == 'POST'):
        print('start')
        form = NewPostForm(request.POST)
        if form.is_valid():
            print("hello")
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
    return redirect(reverse('homePage'))

class AvatarChangeForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(AvatarChangeForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'custom-file-input'})

def homePage(request):
    return redirect('/user/' + request.user.username)

class SubscribeForm(forms.Form):
    user = forms.CharField(widget=forms.HiddenInput())

def subscribe(request):
    if (request.method == 'POST'):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.get(username=request.user.username).friends.add(
                User.objects.get(username=data['user'])
            )
    return redirect(request.META.get('HTTP_REFERER'))

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
    template_name = 'user.html'
    slug_field = 'username'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        currUser = User.objects.get(username=self.kwargs['slug'])

        newPostForm = NewPostForm()
        subscribeForm = SubscribeForm({'user' : self.kwargs['slug']})
        posts = Post.objects.filter(creator=currUser).order_by('-time')
        friends = currUser.friends.all()
        changeAvatarForm = AvatarChangeForm()

        context['newPostForm'] = newPostForm
        context['subscribeForm'] = subscribeForm
        context['posts'] = posts
        context['friends'] = friends
        context['avatarChangeForm'] = changeAvatarForm
        return context



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar']



class UserRegistration(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'


class FriendListVeiw(CreateView):

    model = User
    fields = ['username', 'avatar', 'first_name', 'last_name']
    template_name = 'friends.html'

    def get_context_data(self, **kwargs):
        context = super(FriendListVeiw, self).get_context_data(**kwargs)
        currUser = User.objects.get(username=self.request.user.username)
        friends = currUser.friends.all().order_by('-first_name')

        context['user_profile'] = currUser
        context['friends'] = friends
        return context

class FeedListVeiw(CreateView):
    model = Post
    fields = []
    template_name = 'feed.html'

    def get_context_data(self, **kwargs):
        context = super(FeedListVeiw, self).get_context_data(**kwargs)
        currUser = User.objects.get(username=self.request.user.username)
        posts = Post.objects.filter(creator=currUser)
        friends = currUser.friends.all().order_by('-first_name')
        for friend in friends:
            posts = sorted(
                chain(posts, Post.objects.filter(creator=friend)),
                key=attrgetter('time'), reverse=True)
        context['user_profile'] = currUser
        context['posts'] = posts
        return context
    # Create your views here.



def changeAvatar(request):
    if (request.method == 'POST'):
        form = AvatarChangeForm(request.POST, request.FILES)
        print('start...')
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.avatar = request.FILES['file']
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))