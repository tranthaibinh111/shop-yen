from django.contrib import admin
from shop_yen.models import *
from .service import ServicePriceAdmin
from .customer import CustomerAdmin
from .provider import ProviderAdmin
from .product import ProductAdmin
from .price import PriceAdmin
from .order import OrderAdmin
from .order_detail import OrderDetailAdmin
from .stock_in import StockInAdmin
from .stock import StockAdmin
from .shipper import ShipperAdmin
from .delivery import DeliveryAdmin
from .advertisement import AdvertisementAdmin
from .cron_advertisement import CronAdvertisementAdmin
from .advertisement_history import AdvertisementHistoryAdmin

# Fee
admin.site.register(Service, ServicePriceAdmin)
# Customer
admin.site.register(Customer, CustomerAdmin)
# Product
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
# Order
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
# Stock
admin.site.register(StockIn, StockInAdmin)
admin.site.register(Stock, StockAdmin)
# Delivery
admin.site.register(Shipper, ShipperAdmin)
admin.site.register(Delivery, DeliveryAdmin)
# Advertisement
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(CronAdvertisement, CronAdvertisementAdmin)
admin.site.register(AdvertisementHistory, AdvertisementHistoryAdmin)
