from datetime import datetime
from django.core.mail import send_mail
from smtplib import SMTPException
from shop_yen.models import *


class CronAdvertisementService:
    def __init__(self, email="Yến Vàng Miền Name <no-reply@yenvangmiennam.com>", limit=100):
        self.email = email
        self.limit = limit

    @classmethod
    def send_email(cls, cron_advertisements: list):
        for cron in cron_advertisements:
            # Update cron status
            cron.status = CronStatus.S.name
            cron.save()
            # Send advertisement email
            try:
                from_email = cls.email
                recipient_list = [cron.customer.contact]
                subject = cron.advertisement.subject
                message = cron.advertisement.content
                send_mail(subject, message, from_email, recipient_list)

                # Create advertisement history
                now = datetime.now()
                AdvertisementHistory.objects.create(
                    advertisement=cron.advertisement,
                    customer=cron.customer,
                    start_at=cron.start_at,
                    done_at=now,
                    status=CronStatus.D.name,
                    created_by=cron.created_by,
                    created_date=cron.create_date,
                    modified_by=cron.modified_by,
                    modified_date=now
                )
                # Remove cron when the process is done
                cron.delete()
            except SMTPException:
                cron.status = CronStatus.E.name
                cron.save()

    @classmethod
    def send_email_auto(cls):
        cron_advertisements = CronAdvertisement.objects.filter(status=CronStatus.W.name)[:100]
        cls.send_email(cron_advertisements)
