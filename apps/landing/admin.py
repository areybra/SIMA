from django.contrib import admin

from .models import Berita, ContactMessage


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'views', 'is_published', 'is_featured', 'created_at')
    list_filter = ('kategori', 'is_published', 'is_featured')
    search_fields = ('judul', 'ringkasan')
    prepopulated_fields = {'slug': ('judul',)}
    readonly_fields = ('views',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'subjek', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('nama', 'email', 'subjek', 'pesan')
    list_editable = ('is_read',)
