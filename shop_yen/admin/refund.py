from django.contrib import admin


class StockOutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Detail', {
            'fields': ('order_detail',)
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
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
