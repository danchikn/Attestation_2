from django.contrib import admin
from .models import User, Item
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Fields", {"fields": ("role",)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Item)
