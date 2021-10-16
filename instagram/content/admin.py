from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from content.models import Post, Tag, Media, TaggedUser, Tag, Like, Stream

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Media)
admin.site.register(TaggedUser)
admin.site.register(Like)
admin.site.register(Stream)


# fix this ... below not working #  #   #   #   #
# class PostAdmin(admin.ModelAdmin):
#     filter_horizontal = ('Post',)

# class LikeInline(admin.TabularInline):
#     model = Like


# class PostTagInline(admin.TabularInline):
#     model = PostTag


# class MediaInline(admin.TabularInline):
#     model = Media
#
#
# class TaggedUserInline(admin.TabularInline):
#     model = TaggedUser
#
#
# @register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['caption', 'user']
#     inlines = [TaggedUserInline]
#
#
# @register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['title', 'created_time']
