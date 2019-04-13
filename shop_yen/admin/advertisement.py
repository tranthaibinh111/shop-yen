from django.contrib import admin


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('advertise_type', 'name', 'start_at', 'subject')
    ordering = ('-modified_date',)
    search_fields = ('name', 'start_at')
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
