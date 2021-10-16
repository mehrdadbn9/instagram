from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated_"), auto_now=True)

    class Meta:
        abstract = True


