import pytz
import uuid
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models
from enum import Enum
from mvc.models import *
from .customer import Customer


class OrderStatus(Enum):
    # Received
    R = "Nhận đơn đặt hàng"
    # Delivering
    D = "Đang chuyển hàng"
    # Completed
    CL = "Đơn hàng hoàn thành"
    # Refunded
    RF = "Đơn hàng đổi trả"
    # Cancelled
    CC = "Đơn hàng bị hủy"


class Order(models.Model):
    __STATUS_CHOICES = [(tag.name, tag.value) for tag in OrderStatus]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(default=OrderStatus.R.name, max_length=2, choices=__STATUS_CHOICES)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    money_of_sale = models.DecimalField(default=0, max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    service = ArrayField(models.IntegerField())
    fee = models.DecimalField(default=0, max_digits=15, decimal_places=0, validators=[MinValueValidator(0)])
    income = models.DecimalField(default=0, max_digits=16, decimal_places=0, validators=[MinValueValidator(0)])
    note = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_order')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_order')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        create_date = self.created_date.astimezone(pytz.timezone(settings.TIME_ZONE))
        return "{} buy {} product at {}".format(self.customer, self.amount, create_date)
