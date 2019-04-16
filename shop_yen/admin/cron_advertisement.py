from django.contrib import admin


class CronAdvertisementAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Advertisement', {
            'fields': ('advertisement',)
        }),
        ('Customer', {
            'fields': ('customer',)
        }),
        ('Cron', {
            'fields': ('start_at', 'status',)
        }),
        ('Staff', {
            'fields': ('created_by', 'created_date', 'modified_by', 'modified_date')
        }),
    )
    list_display = ('advertisement', 'customer', 'start_at', 'status')
    ordering = ('-modified_date',)
    search_fields = ('customer.first_name', 'customer.last_name', 'customer.contact')
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
