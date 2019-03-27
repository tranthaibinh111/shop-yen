from django.contrib import admin
from shop_yen.models import *
from .customer import CustomerAdmin

admin.site.register(Customer, CustomerAdmin)
