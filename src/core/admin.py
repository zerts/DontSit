# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Achievment


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (u'Дополнительно', {'fields': ('avatar',)}),
    )

    def admin_avatar(self, instance):
        return instance.avatar and \
               u'<img src="/media/avatars/admin.jpg" width="100px" />'.format(
            instance.avatar.url
        )

    admin_avatar.allow_tags = True
    admin_avatar.short_description = u'Аватар'


admin.site.register(User, UserAdmin)


@admin.register(Achievment)
class AchievmentAdmin(admin.ModelAdmin):
    pass
