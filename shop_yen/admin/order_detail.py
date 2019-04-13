from django.contrib import admin
from django.core.exceptions import ValidationError
from shop_yen.models import *


class OrderDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order', {
            'fields': ('order',)
        }),
        ('Detail', {
            'fields': ('product', 'status', 'price', 'amount')
        }),
        ('Pay', {
            'fields': ('money_of_sale',)
        }),
        ('Staff', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('customer', 'product', 'price', 'amount', 'money_of_sale', 'created_by', 'modified_by')
    ordering = ('-modified_date',)
    search_fields = ('order.customer.first_name', 'order.customer.last_name', 'order.customer.contact')
    readonly_fields = ('money_of_sale', 'created_by', 'created_date', 'modified_by', 'modified_date')

    def customer(self, obj):
        return obj.order.customer.name

    def save_model(self, request, obj, form, change):
        # Check price
        price = Price.objects.filter(product=obj.product).first()
        if obj.price <= price.cost_of_good:
            raise ValidationError("Tiền bán không được nhỏ hơn tiền nhập hàng")
        # Check stock
        stock = Stock.objects.filter(product=obj.product).first()
        if obj.amount > stock.balance:
            message = "Đã hết hàng. Số lượng trong kho là {}".format(stock.balance)
            raise ValidationError(message)
        # Calculate money of sale
        obj.money_of_sale = obj.price * obj.amount
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            if obj.status != OrderDetail.R.name:
                raise ValidationError("Khởi tạo hóa đơn ban đầu phải ở trạng thái 'Nhận đơn đặt hàng'")
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
