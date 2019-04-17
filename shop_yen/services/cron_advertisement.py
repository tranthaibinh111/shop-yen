from datetime import datetime
from django.core.mail import EmailMessage
from django.db.models import Q
from smtplib import SMTPException
from shop_yen.models import *


class CronAdvertisementService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if CronAdvertisementService.__instance == None:
            CronAdvertisementService()
        return CronAdvertisementService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CronAdvertisementService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CronAdvertisementService.__instance = self

    @classmethod
    def send_email(cls, cron_advertisements: list, from_email: str):
        for cron in cron_advertisements:
            # Update cron status
            cron.status = CronStatus.S.name
            cron.save()
            # Send advertisement email
            try:
                recipient_list = [cron.customer.contact]
                subject = cron.advertisement.subject
                body = cron.advertisement.content
                # https://docs.djangoproject.com/en/2.2/topics/email/
                msg = EmailMessage(subject, body, from_email, recipient_list)
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

                # Create advertisement history
                now = datetime.now()
                AdvertisementHistory.objects.create(
                    advertisement=cron.advertisement,
                    customer=cron.customer,
                    start_at=cron.start_at,
                    done_at=now,
                    status=CronStatus.D.name,
                    created_by=cron.created_by,
                    created_date=cron.created_date,
                    modified_by=cron.modified_by,
                    modified_date=now
                )
                # Remove cron when the process is done
                cron.delete()
            except SMTPException:
                cron.status = CronStatus.E.name
                cron.save()

    @classmethod
    def send_email_auto(
            cls,
            now=datetime.now(),
            from_email="Yến Vàng Miền Name <advertisement@yenvangmiennam.com>",
            limit=100):
        cron_advertisements = CronAdvertisement.objects.filter(
            Q(status=CronStatus.W.name) &
            Q(start_at__lte=now)
        )[:limit]
        cls.send_email(cron_advertisements, from_email)
