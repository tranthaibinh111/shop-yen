from django.contrib import admin


class ServicePriceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Service', {
            'fields': ('name', 'price')
        }),
        ('Note', {
            'fields': ('note',)
        })
    )
    list_display = ('name', 'price', 'note')
    ordering = ('-modified_date',)
    search_fields = ('name',)
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        # Case update or new
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
