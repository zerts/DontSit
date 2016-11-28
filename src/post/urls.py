from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from post.views import PostLikesView, PostLikes

urlpatterns = [
    url(r'(?P<pk>\d+)/likes/$', PostLikesView.as_view(), name='likes'),
    url(r'likes/$', PostLikes.as_view(), name='likes_all')
]