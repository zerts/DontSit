from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from views import UserView, RegisterForm, subscribe, newPost

urlpatterns = [
    url(r'register/$', CreateView.as_view(
            form_class=RegisterForm,
            template_name='registration.html',
            success_url=reverse_lazy('core:login')
        )),
    url(r'login/$', login, kwargs={'template_name' : 'core/login.html',}, name='login'),
    url(r'logout/$', logout, kwargs={'template_name' : 'core/logout.html',}, name='logout'),
    url(r'(?P<slug>[\w.@+-]+)/$', UserView.as_view()),
]