from django.contrib import admin
from .models import NavItem

# Register your models here.

@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'url')
