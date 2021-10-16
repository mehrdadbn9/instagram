from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from user.models import User

#
# @admin.register(User)
# class UserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'is_staff')

admin.site.register(User)
