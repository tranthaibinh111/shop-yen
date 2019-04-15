from django.db import models
from .cron_advertisement import CronAdvertisement


class CronAdvertisementHistory(CronAdvertisement):
    done_at = models.DateTimeField(auto_now_add=True)
