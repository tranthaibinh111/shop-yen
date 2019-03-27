from django.contrib import admin
from mvc.models import *
from .user import UserAdmin

admin.site.register(User, UserAdmin)
