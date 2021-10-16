from django.contrib import admin
from django.contrib.admin import register

from activity.models import Comment
from content.models import Like


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'post', 'reply']


# @register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['user', 'post']
