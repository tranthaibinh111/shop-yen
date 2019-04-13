from django.contrib import admin


class ShipperAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'gender', 'note')
    ordering = ('-modified_date',)
    search_fields = ('first_name', 'last_name', 'contact')
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
