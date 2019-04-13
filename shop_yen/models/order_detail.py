import uuid
from django.db import models
from django.core.validators import MinValueValidator
from enum import Enum
from mvc.models import *
from .order import Order
from .product import Product


class OrderDetailStatus(Enum):
    # Out stock
    OS = "Hết hàng"
    # Received
    R = "Nhận đơn đặt hàng"
    # Delivering
    D = "Đang chuyển hàng"
    # Completed
    CL = "Đã giao hàng"
    # Refunded
    RF = "Đơn hàng đổi trả"
    # Cancelled
    CC = "Đơn hàng bị hủy"


class OrderDetail(models.Model):
    __STATUS_CHOICES = [(tag.name, tag.value) for tag in OrderDetailStatus]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(default=OrderDetailStatus.R.name, max_length=2, choices=__STATUS_CHOICES)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=0, validators=[MinValueValidator(0)])
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    money_of_sale = models.DecimalField(default=0, max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_order_detail')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_order_detail')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} buy {} at {}".format(self.order.customer, self.product, self.created_date)

    class Meta:
        unique_together = ('order', 'product')
        verbose_name_plural = "Order Details"
