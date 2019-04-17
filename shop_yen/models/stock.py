import uuid
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from mvc.models import *
from .product import Product


class Stock(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Số lượng thực tế trong kho")
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Số lượng mà khách hàng đang đặt")
    refund = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Số lượng mà khách hàng đang đổi trả")
    balance = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Số lượng dự tính còn lại")
    fee = models.DecimalField(default=0, max_digits=20, decimal_places=0, validators=[MinValueValidator(0)], help_text="Tiền phí nhập hàng")
    fund = models.DecimalField(default=0, max_digits=25, decimal_places=0, validators=[MinValueValidator(0)], help_text="Tổng tiền vốn")
    money_of_sale = models.DecimalField(default=0, max_digits=25, decimal_places=0, validators=[MinValueValidator(0)], help_text="Tổng tiền bán")
    refund_money = models.DecimalField(default=0, max_digits=25, decimal_places=0, validators=[MinValueValidator(0)], help_text="Tổng tiền do khách hàng trả hàng")
    income = models.DecimalField(default=0, max_digits=30, decimal_places=0, validators=[MinValueValidator(0)], help_text="Tiền lời")
    note = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.IntegerField(help_text="Thời gian cuối cùng kiểm kê kho")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_stock')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_stock')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.product, self.retail_price)

    class Meta:
        unique_together = ('product',)
