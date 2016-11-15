"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from core.views import UserListView, newPost, homePage, subscribe, FriendListVeiw, FeedListVeiw, changeAvatar

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^user/', include('core.urls', namespace='core')),
    url(r'^users/$', UserListView.as_view()),
    url(r'^homepage/$', homePage, name='homePage'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^newpost/$', newPost, name='newPost'),
    url(r'^friends/$', FriendListVeiw.as_view(), name='friends'),
    url(r'^feed/$', FeedListVeiw.as_view(), name='feed'),
    url(r'^updateavatar/$', changeAvatar, name='updateAvatar'),
]
