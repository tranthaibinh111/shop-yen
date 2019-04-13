import uuid
from django.db import models
from django.conf import settings
from mvc.models import *


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to="{}/{}".format(settings.PRODUCT_PATH, uuid), null=True, blank=True)
    weight = models.DecimalField(default=0, max_digits=8, decimal_places=1)
    note = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_product')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_product')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        config = Configure.obejct.all().first()
        return "{} {}{}".format(self.name, self.weight, config.unit_weight)

    class Meta:
        unique_together = ('name', 'weight')
