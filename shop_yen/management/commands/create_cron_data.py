#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from mvc.models import *
from shop_yen.models import *


class Command(BaseCommand):
    help = 'Create Cron Data which help run advertisement email'

    def add_arguments(self, parser):
        parser.add_argument('advertisement_id', type=int)
        parser.add_argument('start_at', type=str)

    def handle(self, *args, **options):
        print("Bắt đầu khởi tạo cron data")
        try:
            advertisement_id = options['advertisement_id']
            start_at = parse_datetime(options["start_at"])
            if advertisement_id and start_at:
                crons = list()
                admin = User.objects.filter(email="admin@yenvangmiennam.com").first()
                customers = Customer.objects.filter(contact_type=ContactChoice.E.name)
                for cus in customers:
                    cron = CronAdvertisement.objects.filter(
                        Q(advertisement_id=advertisement_id) &
                        Q(customer=cus) &
                        Q(start_at=start_at)
                    )
                    if not cron.exists():
                        crons.append(CronAdvertisement(
                            advertisement_id=advertisement_id,
                            customer=cus,
                            start_at=start_at,
                            created_by=admin,
                            modified_by=admin
                        ))
                        # Create cron advertisement when count = 100
                        if len(crons) >= 100:
                            CronAdvertisement.objects.bulk_create(crons)
                            crons.clear()
                # Case crons > 0 and crons < 100
                if len(crons) > 0:
                    CronAdvertisement.objects.bulk_create(crons)
                    crons.clear()
        except Exception as ex:
            print(ex)
        print("Kết thúc tạo cron data")
