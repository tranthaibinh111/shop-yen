from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Sum
from shop_yen.models import *


class StockInAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Provider', {
            'fields': ('provider', 'product')
        }),
        ('Product', {
            'fields': ('price', 'amount')
        }),
        ('Service', {
            'fields': ('service',)
        }),
        ('Fund', {
            'fields': ('cost_of_good', 'fee', 'fund')
        }),
        ('Staff', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('provider', 'product', 'amount', 'cost_of_good', 'fee', 'fund', 'created_by', 'modified_by')
    ordering = ('-modified_date',)
    search_fields = ('provider.name', 'product.name')
    readonly_fields = ('cost_of_good', 'fee', 'fund', 'created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        # Check price
        price = Price.objects.filter(product=obj.product).first()
        if obj.price != price.cost_of_good:
            raise ValidationError("Giá tiền không đúng với thông tin Price")
        # Calculate cost of good
        obj.cost_of_good = obj.price * obj.amount
        # Calculate fee
        fee = 0
        for item in Service.objects.filter(pk__in=obj.service):
            fee += item.price
        obj.fee = fee
        # Calculate fund
        obj.fund = obj.cost_of_good + obj.fee
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
        # Update amount product in Stock
        stock_in = StockIn.object.filter(
            product=obj.product
        ).aggregate(
            total_amount=Sum('amount'),
            total_fee=Sum('fee'),
            total_fund=Sum('fund')
        )
        stock = Stock.Object.filter(product=obj.product).first()
        stock.amount = stock_in.get('total_amount')
        stock.balance = stock.amount - stock.order
        stock.fee = stock_in.get('total_fee')
        stock.fund = stock_in.get('total_fund')
        stock.income = stock.money_of_sale - (stock.fund + stock.fee)
