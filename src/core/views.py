from datetime import datetime
from itertools import chain
from operator import attrgetter

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView, ListView
from django.views.generic import FormView

from post.models import Post
from post.views import EditPostForm
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
    return redirect(reverse('homePage'))

class AvatarChangeForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(AvatarChangeForm, self).__init__(*args, **kwargs)

class UsernameChangeForm(forms.Form):
    firstName = forms.CharField()
    lastName = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(UsernameChangeForm, self).__init__(*args, **kwargs)

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
        editPostForm = EditPostForm()
        subscribeForm = SubscribeForm({'user' : self.kwargs['slug']})
        posts = Post.objects.all().show_my(currUser)
        posts = posts.select_related('creator')
        #posts = Post.objects.filter(creator=currUser).order_by('-time')
        friends = currUser.friends.all()
        changeAvatarForm = AvatarChangeForm()
        changeUsernameForm = UsernameChangeForm()

        context['newPostForm'] = newPostForm
        context['editPostForm'] = editPostForm
        context['subscribeForm'] = subscribeForm
        context['posts'] = posts
        context['friends'] = friends
        context['avatarChangeForm'] = changeAvatarForm
        context['usernameChangeForm'] = changeUsernameForm
        return context



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'avatar']



class UserRegistration(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('core:login')

    def form_valid(self, form):
        print("hello")
        if not form.instance.avatar:
            form.instance.avatar = "/avatars/default.png"
        if not form.instance.first_name:
            form.instance.first_name = "First"
        if not form.instance.last_name:
            form.instance.last_name = "last"
        form.save()
        return super(UserRegistration, self).form_valid(form)



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
        posts = Post.objects.all().show_my(currUser)
        posts = posts.select_related('creator')
        #posts = Post.objects.filter(creator=currUser)
        friends = currUser.friends.all().order_by('-first_name')
        for friend in friends:
            posts = sorted(
                chain(posts, Post.objects.all().show_my(friend)),
                key=attrgetter('time'), reverse=True)
        context['user_profile'] = currUser
        context['posts'] = posts
        return context
    # Create your views here.



def changeAvatar(request):
    if (request.method == 'POST'):
        form = AvatarChangeForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.avatar = request.FILES['file']
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))

def changeName(request, slug):
    if (request.method == 'POST'):
        form = UsernameChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(username=slug)
            user.first_name = data['firstName']
            user.last_name = data['lastName']
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))