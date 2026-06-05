from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password", "is_active")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    ordering = ["email"]
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2", "is_active")}),
    )
