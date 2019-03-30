from django.contrib import admin
from django.contrib.auth.hashers import make_password
from mvc.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_superuser', 'is_staff', 'is_active', 'timezone')
    ordering = ('first_name', 'last_name', 'pk')
    search_fields = ('first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        if change:
            old_pass = User.objects.get(pk=obj.pk).password
            if old_pass != obj.password:
                obj.password = make_password(obj.password)
        else:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
