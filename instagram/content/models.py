import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete

# from activity.models import Like
from relation.models import Relation
from utils import BaseModel
from notification.models import Notification

# from location.models import Location

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(BaseModel):
    title = models.CharField(_("title"), max_length=32)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Like(BaseModel):
    like = models.IntegerField(default=0)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()


class Media(BaseModel):
    IMAGE = 1
    VIDEO = 2

    TYPE_CHOICES = (
        (IMAGE, _("image")),
        (VIDEO, _("video"))
    )
    # media_type = models.PositiveSmallIntegerField(_("media"), choices=TYPE_CHOICES)  # should hav default??
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_owner')
    # post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to=user_directory_path, validators=[
        FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))])

    # def __str__(self):
    #     return f"{self.get_media_type_display()}"


class Post(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField(_('caption'), blank=True, max_length=1500, )
    likes = models.ManyToManyField(Like, related_name='likes', blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    media = models.ManyToManyField(Media, related_name='media')

    # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="posts",
    # blank=True)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])

    def __str__(self):
        return str(self.id)


# class PostTag(BaseModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hashtags')
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts')
#
#     class Meta:
#         verbose_name = _("PostTag")
#         verbose_name_plural = _("PostsTags")
#
#     def __str__(self):
#         return f"{self.post} - {self.tag}"


class TaggedUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tagged_post")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tagged_user")

    class Meta:
        verbose_name = _("TaggedUser")
        verbose_name_plural = _("TaggedUsers")

    def __str__(self):
        return f"{self.user} - {self.post}"


class Stream(BaseModel):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Relation.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, created_time=post.created_time, following=user)
            stream.save()


# Stream
post_save.connect(Stream.add_post, sender=Post)

# Likes
post_save.connect(Like.user_liked_post, sender=Like)
post_delete.connect(Like.user_unlike_post, sender=Like)

