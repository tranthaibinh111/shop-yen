from celery import shared_task
from .services import *


@shared_task
def send_advertisement_email():
    cron = CronAdvertisementService.get_instance()
    cron.send_email_auto()
