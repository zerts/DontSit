from django.contrib import admin

# Register your models here.
from post.models import Post, Note, Comment, Like


@admin.register(Note)
class MyFriendAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class AchievmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class MyFriendAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class AchievmentAdmin(admin.ModelAdmin):
    pass
