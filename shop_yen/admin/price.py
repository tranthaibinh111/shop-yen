from django.contrib import admin


class PriceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Provide', {
            'fields': ('provider', 'product')
        }),
        ('Price', {
            'fields': ('apply_date', 'cost_of_good', 'regular_price', 'retail_price', 'is_active')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('provider', 'product', 'apply_date', 'cost_of_good', 'regular_price', 'retail_price')
    ordering = ('-modified_date',)
    search_fields = ('provider.name',)
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
