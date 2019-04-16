from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from shop_yen.models import *


class DeliveryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Shipper', {
            'fields': ('shipper', 'from_place', 'to_place')
        }),
        ('Order Detail', {
            'fields': ('order_detail', 'status')
        }),
        ('Staff', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('order', 'product', 'amount', 'money_of_sale', 'from_place', 'to_place', 'shipper')
    ordering = ('-modified_date',)
    search_fields = (
        'order_detail.order.customer.first_name',
        'order_detail.order.customer.last_name',
        'order_detail.order.customer.contact'
    )
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def order(self, obj):
        return obj.order_detail.order

    def product(self, obj):
        return obj.order_detail.product

    def amount(self, obj):
        return obj.order_detail.amount

    def money_of_sale(self, obj):
        return obj.order_detail.money_of_sale

    def save_model(self, request, obj, form, change):
        if obj.order.status == OrderStatus.CC.name:
            raise ValidationError("Đơn hàng đã hủy khỏi cần giao")
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            if obj.status != DeliveryStatus.D.name:
                raise ValidationError("Khởi tạo hóa đơn ban đầu phải ở trạng thái 'Đang chuyển hàng'")
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

        if obj.status == DeliveryStatus.D.name:
            # Update status order detail
            obj.order_detail.status = OrderDetailStatus.D.name
            obj.order_detail.save()
            # Update stock out
            StockOut.objects.create(
                order_detail=obj.order_detail,
                created_by=obj.created_by,
                modified_by=obj.modified_by
            )
            # Update stock
            stock_out = StockOut.objects.filter(
                Q(order_detail__product=obj.order_detail.product) &
                Q(order_detail__status=OrderDetailStatus.D.name)
            ).aggregate(
                total_order=Sum('amount'),
                total_money_of_sale=Sum('money_of_sale')
            )
            stock = Stock.objects.filter(product=obj.order_detail.product).first()
            stock.order = stock_out.get('total_order')
            stock.money_of_sale = stock_out.get('total_money_of_sale')
            stock.income = (stock.money_of_sale - stock.refund_money) - (stock.fund + stock.fee)
            # Update status order
            order = Order.objects.filter(pk=obj.order_detail.order.pk).first()
            order_status = OrderStatus.D.name
            order_details = OrderDetail.objects.filter(
                Q(order=order) &
                ~Q(status__in=[OrderDetailStatus.OS.name, OrderDetailStatus.CL.name, OrderDetailStatus.RF.name])
            )
            for item in order_details:
                if item.status != OrderDetailStatus.D.name:
                    order_status = OrderStatus.R.name
                    break
            order.status = order_status
            order.status = obj.created_by
            order.save()
        elif obj.status == DeliveryStatus.CL.name:
            # Update status order detail
            obj.order_detail.status = OrderDetailStatus.CL.name
            obj.order_detail.save()
            # Update status order
            order = Order.objects.filter(pk=obj.order_detail.order.pk).first()
            order_status = OrderStatus.CL.name
            order_details = OrderDetail.objects.filter(
                Q(order=order) &
                ~Q(status__in=[OrderDetailStatus.OS.name, OrderDetailStatus.CL.name, OrderDetailStatus.RF.name])
            )
            for item in order_details:
                if item.status != OrderDetailStatus.CL.name:
                    order_status = OrderStatus.D.name
                    break
            if order_status == OrderStatus.D.name:
                order.status = order_status
                order.status = obj.created_by
                order.save()
        else:
            # Update status order detail
            obj.order_detail.status = OrderDetailStatus.RF.name
            obj.order_detail.save()
            # Update status order
            obj.order_detail.order.status = OrderStatus.RF.name
            # Update Refund
            Refund.objects.create(
                order_detail=obj.order_detail,
                created_by=obj.created_by,
                modified_by=obj.modified_by
            )
            # Update stock
            refund = Refund.objects.filter(
                order_detail__product=obj.order_detail.product
            ).aggregate(
                total_refund=Sum('amount'),
                total_refund_money=Sum('money_of_sale')
            )
            stock = Stock.objects.filter(product=obj.order_detail.product).first()
            stock.refund = refund.get('total_refund')
            stock.refund_money = refund.get('total_refund_money')
            stock.income = (stock.money_of_sale - stock.refund_money) - (stock.fund + stock.fee)
