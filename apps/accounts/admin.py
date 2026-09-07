from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Peran SIMA', {'fields': ('role', 'no_hp')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Peran SIMA', {'fields': ('role', 'no_hp')}),
    )
