from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import MenuItem


class MenuItemAdmin(MPTTModelAdmin):
    pass


admin.site.register(MenuItem, MenuItemAdmin)
