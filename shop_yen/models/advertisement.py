import pytz
from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from enum import Enum
from mvc.models import *


class AdvertisementType(Enum):
    E = "Email"
    F = "Facebook"


class Advertisement(models.Model):
    __TYPE_CHOICES = [(tag.name, tag.value) for tag in AdvertisementType]

    advertise_type = models.CharField(max_length=2, choices=__TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_advertisement')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_advertisement')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        start_at = self.start_at.astimezone(pytz.timezone(settings.TIME_ZONE))
        return "{} {}".format(self.name, start_at)

    class Meta:
        unique_together = ('advertise_type', 'name', 'start_at')
