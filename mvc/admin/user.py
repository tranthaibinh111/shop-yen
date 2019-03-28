from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('password', )
    list_display = ('name', 'email', 'is_superuser', 'is_staff', 'is_active', 'timezone')
    ordering = ('first_name', 'last_name', 'pk')
    search_fields = ('first_name', 'last_name')
