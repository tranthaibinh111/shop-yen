import uuid
from django.db import models
from enum import Enum
from mvc.models import *
from .advertisement import Advertisement
from .customer import Customer


class CronStatus(Enum):
    # Waiting
    W = "Đang chờ chạy quảng cáo"
    # Starting
    S = "Đang gửi quảng cáo"
    # Done
    D = "Hoàn thành"
    # Error
    E = "Gửi quảng cáo thất bại"


class CronAdvertisement(models.Model):
    __STATUS_CHOICES = [(tag.name, tag.value) for tag in CronStatus]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default=CronStatus.W.name, max_length=2, choices=__STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_marketplace')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_marketplace')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.status, self.customer)

    class Meta:
        verbose_name_plural = "Cron Advertisements"
