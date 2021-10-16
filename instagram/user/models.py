import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from PIL import Image


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user/user_{0}/profile.jpg'.format(instance.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


class User(AbstractBaseUser, PermissionsMixin):  ###for using permisions & Group  mixin added
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=True)
    phone_number = models.CharField(_("phone number"), blank=True, max_length=11)
    location = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

    # avatar = models.ImageField(upload_to='user/avatar/', width_field=150, height_field=166, blank=True)
    bio = models.TextField(_("bio"), blank=True)
    website = models.URLField(_("website"), blank=True)
    is_verified = models.BooleanField(_("is verified"), default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    followers_count = models.PositiveSmallIntegerField(default=0)
    followings_count = models.PositiveSmallIntegerField(default=0)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250

        if self.avatar:
            pic = Image.open(self.avatar.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.avatar.path)

    def __str__(self):
        return self.username
