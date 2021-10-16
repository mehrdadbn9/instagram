from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from notification.models import Notification

from utils import BaseModel

User = get_user_model()


class Relation(BaseModel):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification(sender=sender, user=following, notification_type=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
        notify.delete()

    class Meta:
        verbose_name = _("Relation")
        verbose_name_plural = _("Relations")

    def __str__(self):
        return f"{self.following} ===> {self.follower}"


# Follow
post_save.connect(Relation.user_follow, sender=Relation)
post_delete.connect(Relation.user_unfollow, sender=Relation)
