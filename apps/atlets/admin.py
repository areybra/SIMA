from django.contrib import admin

from .models import AtletProfile, Cabor, DokumenAtlet, PerguruanProfil, Prestasi


@admin.register(Cabor)
class CaborAdmin(admin.ModelAdmin):
    list_display = ('nama', 'aktif')
    list_filter = ('aktif',)
    search_fields = ('nama',)


@admin.register(PerguruanProfil)
class PerguruanProfilAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kontak', 'updated_at')


@admin.register(AtletProfile)
class AtletProfileAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'cabor', 'kelas_kategori', 'jenis_kelamin', 'status_aktif')
    list_filter = ('cabor', 'jenis_kelamin', 'status_aktif')
    search_fields = ('nama_lengkap', 'kelas_kategori')


@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('nama_kejuaraan', 'atlet', 'tingkat', 'hasil', 'tahun')
    list_filter = ('tingkat', 'tahun')
    search_fields = ('nama_kejuaraan', 'atlet__nama_lengkap')


@admin.register(DokumenAtlet)
class DokumenAtletAdmin(admin.ModelAdmin):
    list_display = ('label', 'atlet', 'uploaded_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('label', 'atlet__nama_lengkap', 'keterangan')
