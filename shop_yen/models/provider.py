from django.db import models
from mvc.models import *


class Provider(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    zalo = models.CharField(max_length=20, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_provider')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_provider')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('name', 'mobile'),
            ('name', 'phone'),
            ('name', 'email'),
            ('name', 'facebook'),
            ('name', 'zalo')
        )
