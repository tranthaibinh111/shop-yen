import uuid
from django.db import models
from mvc.models import *
from .order_detail import OrderDetail


class StockOut(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_stock_out')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_stock_out')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.order.product, self.order.total)

    class Meta:
        verbose_name_plural = "Stock Outs"
