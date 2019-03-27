from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'gender')
    ordering = ('first_name', 'last_name', 'pk')
    search_fields = ('first_name', 'last_name', 'contact')
