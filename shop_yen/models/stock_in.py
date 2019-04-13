import uuid
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from mvc.models import *
from .product import Product
from .provider import Provider


class StockIn(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cost_of_good = models.DecimalField(default=0, max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    service = ArrayField(models.IntegerField())
    fee = models.DecimalField(default=0, max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    fund = models.DecimalField(default=0, max_digits=16, decimal_places=0, validators=[MinValueValidator(0)])
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_stock_in')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_stock_in')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.product, self.fund)

    class Meta:
        verbose_name_plural = "Stock Ins"
