from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField

from utils import BaseModel

"""
it contains lat, long and maybe tags or it could simply replace by GeoDjango
"""


# class Location(BaseModel):
#     points = models.JSONField(null=True, default=dict)
#     title = models.CharField(_("title"), max_length=50)
#
#     class Meta:
#         verbose_name = _("Location")
#         verbose_name_plural = _("Locations")
#
#     def __str__(self):
#         return self.title
