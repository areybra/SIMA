from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'subjek', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('nama', 'email', 'subjek', 'pesan')
    list_editable = ('is_read',)
