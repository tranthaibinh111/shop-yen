from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Customer', {
            'fields': ('customer',)
        }),
        ('Info', {
            'fields': ('status', 'amount', 'service')
        }),
        ('Pay', {
            'fields': ('money_of_sale', 'fee', 'income')
        }),
        ('Staff', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('customer', 'status', 'amount', 'money_of_sale', 'fee', 'income', 'created_by', 'modified_by')
    ordering = ('-modified_date',)
    search_fields = ('customer.first_name', 'customer.last_name', 'customer.contact')
    readonly_fields = (
        'status',
        'amount',
        'money_of_sale',
        'fee',
        'income',
        'created_by',
        'created_date',
        'modified_by',
        'modified_date'
    )

    def customer(self, obj):
        return obj.customer.name

    def save_model(self, request, obj, form, change):
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
