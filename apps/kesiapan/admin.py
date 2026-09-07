from django.contrib import admin

from .models import PenilaianKesiapan


@admin.register(PenilaianKesiapan)
class PenilaianKesiapanAdmin(admin.ModelAdmin):
    list_display = ('atlet', 'tanggal', 'fisik', 'teknik', 'mental', 'kehadiran', 'ada_cedera')
    list_filter = ('tanggal', 'kehadiran', 'ada_cedera', 'atlet__cabor')
    search_fields = ('atlet__nama_lengkap', 'catatan_pelatih')
    date_hierarchy = 'tanggal'
