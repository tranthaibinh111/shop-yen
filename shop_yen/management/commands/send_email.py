#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Insert customer info from excel file'

    def handle(self, *args, **options):
        from_email = "sport@yenvangmiennam.com"
        to_email = "yenvangmiennam@yenvangmiennam.com"

        subject = "Sending with SendGrid is Fun"
        content = "and easy to do anywhere, even with Python"

        response = send_mail(
            subject=subject,
            message=content,
            from_email=from_email,
            recipient_list=[to_email]
        )

        print(response)
