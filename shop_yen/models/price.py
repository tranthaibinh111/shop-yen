from django.db import models
from django.core.validators import MinValueValidator
from mvc.models import *
from .provider import Provider
from .product import Product


class Price(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    apply_date = models.DateTimeField(auto_now_add=True, help_text="Thời gian bắt đầu áp dụng giá")
    cost_of_good = models.DecimalField(default=0, max_digits=9, decimal_places=0, validators=[MinValueValidator(0)], help_text="Giá vốn")
    regular_price = models.DecimalField(default=0, max_digits=9, decimal_places=0, validators=[MinValueValidator(0)], help_text="Giá vốn")
    retail_price = models.DecimalField(default=0, max_digits=9, decimal_places=0, validators=[MinValueValidator(0)], help_text="Giá vốn")
    note = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_price')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_price')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.product, self.money)

    class Meta:
        unique_together = ('provider', 'product', 'apply_date')
