from django.db import models

from apps.atlets.models import Cabor


class JadwalLatihan(models.Model):
    class Hari(models.TextChoices):
        SENIN = 'Senin', 'Senin'
        SELASA = 'Selasa', 'Selasa'
        RABU = 'Rabu', 'Rabu'
        KAMIS = 'Kamis', 'Kamis'
        JUMAT = 'Jumat', 'Jumat'
        SABTU = 'Sabtu', 'Sabtu'
        MINGGU = 'Minggu', 'Minggu'

    cabor = models.ForeignKey(
        Cabor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='jadwal', help_text='Kosongkan = berlaku umum/semua cabor.',
    )
    hari = models.CharField(max_length=10, choices=Hari.choices)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    lokasi = models.CharField(max_length=200)
    pelatih = models.CharField(max_length=150, blank=True)
    kelompok = models.CharField(max_length=150, blank=True, help_text='Contoh: Junior / Senior / Semua')
    keterangan = models.TextField(blank=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ['hari', 'jam_mulai']
        verbose_name = 'Jadwal Latihan'
        verbose_name_plural = 'Jadwal Latihan'

    def __str__(self):
        cabor = self.cabor.nama if self.cabor else 'Umum'
        return f'{self.hari} {self.jam_mulai}-{self.jam_selesai} | {cabor} @ {self.lokasi}'


class AgendaEvent(models.Model):
    class Jenis(models.TextChoices):
        LAT_GAB = 'latihan_gabungan', 'Latihan Gabungan'
        TRYOUT = 'tryout', 'Try Out / Uji Tanding'
        KEJUARAAN = 'kejuaraan', 'Kejuaraan'
        RAPAT = 'rapat', 'Rapat / Pembinaan'
        LAINNYA = 'lainnya', 'Lainnya'

    nama = models.CharField(max_length=200)
    jenis = models.CharField(max_length=20, choices=Jenis.choices, default=Jenis.LAT_GAB)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(null=True, blank=True)
    lokasi = models.CharField(max_length=200, blank=True)
    cabor = models.ForeignKey(Cabor, on_delete=models.SET_NULL, null=True, blank=True, related_name='agenda')
    deskripsi = models.TextField(blank=True)

    class Meta:
        ordering = ['tanggal_mulai']
        verbose_name = 'Agenda / Event'
        verbose_name_plural = 'Agenda / Event'

    def __str__(self):
        return f'{self.nama} ({self.tanggal_mulai})'
