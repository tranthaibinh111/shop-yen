from django.db import models
from django.core.validators import MinValueValidator
from mvc.models import *


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_service_price')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_service_price')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.name, self.price)

    class Meta:
        verbose_name_plural = "Service Prices"
