#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from shop_yen.services import *


class Command(BaseCommand):
    help = 'Insert customer info from excel file'

    def handle(self, *args, **options):
        folder_path = "{}/{}".format(settings.BASE_DIR, settings.PATH_IMPORT_EXCEL)
        print("Begin read excel import")
        for file in os.listdir(folder_path):
            path_to_file = "{}/{}".format(folder_path, file)
            service = CustomerService()
            customers = service.import_excel(path_to_file)
            service.insert_customers(customers)
        print("End!")
