from django.contrib import admin


class StockAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Product', {
            'fields': ('product', 'amount', 'order', 'balance')
        }),
        ('Money', {
            'fields': ('fee', 'fund', 'money_of_sale', 'income')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('product', 'amount', 'order', 'balance', 'fee', 'fund', 'money_of_sale', 'income')
    ordering = ('-modified_date',)
    search_fields = ('product.name',)
    readonly_fields = (
        'order',
        'balance',
        'fee',
        'fund',
        'money_of_sale',
        'income',
        'created_by',
        'created_date',
        'modified_by',
        'modified_date'
    )

    def save_model(self, request, obj, form, change):
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
