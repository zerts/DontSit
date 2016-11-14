from datetime import datetime

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
    template_name = 'core/user.html'
    slug_field = 'username'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        currUser = User.objects.get(username=self.kwargs['slug'])

        newPostForm = NewPostForm()
        subscribeForm = SubscribeForm({'user' : self.kwargs['slug']})
        posts = Post.objects.filter(creator=currUser).order_by('-time')
        friends = currUser.friends.all()

        context['newPostForm'] = newPostForm
        context['subscribeForm'] = subscribeForm
        context['posts'] = posts
        context['friends'] = friends
        return context



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar']



class UserRegistration(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'

# Create your views here.
