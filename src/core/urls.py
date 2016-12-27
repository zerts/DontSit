from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from views import UserView, RegisterForm, subscribe, newPost, UserRegistration, changeName

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'register/$', UserRegistration.as_view()),
    url(r'login/$', login, kwargs={'template_name' : 'login.html',}, name='login'),
    url(r'logout/$', logout, kwargs={'template_name' : 'logout.html',}, name='logout'),
    url(r'(?P<slug>[\w.@+-]+)/changeName/$', changeName, name='updateUsername'),
    url(r'(?P<slug>[\w.@+-]+)/$', UserView.as_view(), name='username'),
]