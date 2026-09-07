from django.conf import settings
from django.db import models


class Cabor(models.Model):
    """Master cabang olahraga — diinput super admin via Jazzmin."""
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cabang Olahraga'
        verbose_name_plural = 'Cabang Olahraga'
        ordering = ['nama']

    def __str__(self):
        return self.nama


class PerguruanProfil(models.Model):
    """Profil perguruan untuk landing page — cukup 1 baris, diedit admin."""
    nama = models.CharField(max_length=150, default='Perguruan SIMA')
    tentang = models.TextField(blank=True, help_text='Deskripsi tentang perguruan')
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True)
    alamat = models.CharField(max_length=255, blank=True)
    kontak = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='perguruan/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Perguruan'
        verbose_name_plural = 'Profil Perguruan'

    def __str__(self):
        return self.nama


class AtletProfile(models.Model):
    class JenisKelamin(models.TextChoices):
        LAKI = 'L', 'Laki-laki'
        PEREMPUAN = 'P', 'Perempuan'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='atlet_profile',
        help_text='Akun login atlet (dibuat admin). Boleh kosong untuk data awal.',
    )
    nama_lengkap = models.CharField(max_length=150)
    jenis_kelamin = models.CharField(max_length=1, choices=JenisKelamin.choices, default=JenisKelamin.LAKI)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    cabor = models.ForeignKey(Cabor, on_delete=models.SET_NULL, null=True, blank=True, related_name='atlet')
    kelas_kategori = models.CharField(
        max_length=100, blank=True,
        help_text='Contoh: Kelas 55kg / Sabuk Biru / Junior Putra',
    )
    tahun_masuk = models.PositiveIntegerField(null=True, blank=True)
    tinggi_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    berat_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    status_aktif = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='atlet/', blank=True, null=True)
    no_hp = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama_lengkap']
        verbose_name = 'Profil Atlet'
        verbose_name_plural = 'Profil Atlet'

    def __str__(self):
        cabor = self.cabor.nama if self.cabor else 'Umum'
        return f'{self.nama_lengkap} ({cabor})'


class Prestasi(models.Model):
    class Tingkat(models.TextChoices):
        KOTA = 'kota', 'Kota/Kabupaten'
        PROVINSI = 'provinsi', 'Provinsi'
        NASIONAL = 'nasional', 'Nasional'
        INTERNASIONAL = 'internasional', 'Internasional'

    atlet = models.ForeignKey(AtletProfile, on_delete=models.CASCADE, related_name='prestasi')
    nama_kejuaraan = models.CharField(max_length=200)
    tingkat = models.CharField(max_length=15, choices=Tingkat.choices, default=Tingkat.KOTA)
    hasil = models.CharField(max_length=100, help_text='Contoh: Juara 1 / Emas / Perak / Perunggu')
    tahun = models.PositiveIntegerField()
    bukti = models.FileField(upload_to='prestasi/', blank=True, null=True)

    class Meta:
        ordering = ['-tahun', 'nama_kejuaraan']
        verbose_name_plural = 'Prestasi'

    def __str__(self):
        return f'{self.nama_kejuaraan} — {self.hasil} ({self.atlet.nama_lengkap})'


class DokumenAtlet(models.Model):
    """Dokumen atlet dengan label bebas (KK, KTP, Akta, Ijazah, dll)."""
    atlet = models.ForeignKey(AtletProfile, on_delete=models.CASCADE, related_name='dokumen')
    label = models.CharField(max_length=100, help_text='Contoh: KTP, KK, Akta Kelahiran, Ijazah, Surat Kesehatan, Sertifikat')
    file = models.FileField(upload_to='dokumen/atlet/%Y/%m/')
    keterangan = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='dokumen_upload')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Dokumen Atlet'
        verbose_name_plural = 'Dokumen Atlet'

    def __str__(self):
        return f'{self.label} — {self.atlet.nama_lengkap}'
