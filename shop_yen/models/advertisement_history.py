from django.db import models
from .cron_advertisement import CronAdvertisement


class AdvertisementHistory(CronAdvertisement):
    done_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Advertisement Histories"
