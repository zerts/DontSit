from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

from views import UserView, newPost, UserListView

urlpatterns = [
    url(r'login/$', login, kwargs={'template_name' : 'core/login.html',}),
    url(r'logout/$', logout, kwargs={'template_name' : 'core/logout.html',}),
    url(r'(?P<slug>[\w.@+-]+)/$', login_required(UserView.as_view())),
    #url(r'home/$', login_required(UserView.as_view()))
]