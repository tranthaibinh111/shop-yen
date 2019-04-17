import uuid
from django.db import models
from mvc.models import *
from .advertisement import Advertisement
from .customer import Customer
from .cron_advertisement import CronStatus


class AdvertisementHistory(models.Model):
    __STATUS_CHOICES = [(tag.name, tag.value) for tag in CronStatus]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    done_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default=CronStatus.W.name, max_length=2, choices=__STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_advertisement_history')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_advertisement_history')
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.status, self.customer)

    class Meta:
        verbose_name_plural = "Advertisement Histories"
