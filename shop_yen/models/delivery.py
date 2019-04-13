import uuid
from django.db import models
from enum import Enum
from mvc.models import *
from .shipper import Shipper
from .order_detail import OrderDetail


class DeliveryStatus(Enum):
    # Delivering
    D = "Đang chuyển hàng"
    # Completed
    CL = "Đơn hàng hoàn thành"
    # Refunded
    RF = "Đơn hàng đổi trả"
    # Cancelled
    CC = "Đơn hàng bị hủy"


class Delivery(models.Model):
    __STATUS_CHOICES = [(tag.name, tag.value) for tag in DeliveryStatus]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    status = models.CharField(default=DeliveryStatus.D.name, max_length=2, choices=__STATUS_CHOICES)
    from_place = models.CharField(max_length=255)
    to_place = models.CharField(max_length=255)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_delivery')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_delivery')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} transfer order to {}".format(self.shipper, self.order.customer)

    class Meta:
        verbose_name_plural = "Deliveries"
