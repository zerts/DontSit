from django.conf.urls import url
from django.contrib.auth.views import login, logout


from views import UserView, UserRegistration, changeName

urlpatterns = [
    url(r'register/$', UserRegistration.as_view()),
    url(r'login/$', login, kwargs={'template_name' : 'login.html',}, name='login'),
    url(r'logout/$', logout, kwargs={'template_name' : 'logout.html',}, name='logout'),
    url(r'(?P<slug>[\w.@+-]+)/changeName/$', changeName, name='updateUsername'),
    url(r'(?P<slug>[\w.@+-]+)/$', UserView.as_view(), name='username'),
]