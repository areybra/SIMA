from django.contrib import admin

from .models import AgendaEvent, JadwalLatihan


@admin.register(JadwalLatihan)
class JadwalLatihanAdmin(admin.ModelAdmin):
    list_display = ('hari', 'jam_mulai', 'jam_selesai', 'cabor', 'lokasi', 'aktif')
    list_filter = ('hari', 'cabor', 'aktif')
    search_fields = ('lokasi', 'pelatih')


@admin.register(AgendaEvent)
class AgendaEventAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenis', 'tanggal_mulai', 'lokasi')
    list_filter = ('jenis',)
    search_fields = ('nama', 'lokasi')
