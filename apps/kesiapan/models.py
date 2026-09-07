from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.atlets.models import AtletProfile


class PenilaianKesiapan(models.Model):
    class Kehadiran(models.TextChoices):
        HADIR = 'hadir', 'Hadir'
        IZIN = 'izin', 'Izin'
        SAKIT = 'sakit', 'Sakit'
        ALFA = 'alfa', 'Alfa/Tanpa Keterangan'

    atlet = models.ForeignKey(AtletProfile, on_delete=models.CASCADE, related_name='penilaian')
    tanggal = models.DateField()
    fisik = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    teknik = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    mental = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    vo2max = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        help_text='Contoh: 45.5 (ml/kg/min). Boleh kosong bila belum diukur.',
    )
    berat_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    tinggi_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    kehadiran = models.CharField(max_length=10, choices=Kehadiran.choices, default=Kehadiran.HADIR)
    ada_cedera = models.BooleanField(default=False)
    keterangan_cedera = models.CharField(max_length=255, blank=True)
    catatan_pelatih = models.TextField(blank=True)
    dinilai_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='penilaian_dibuat',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal']
        constraints = [
            models.UniqueConstraint(fields=['atlet', 'tanggal'], name='uniq_penilaian_atlet_tanggal'),
        ]
        verbose_name = 'Penilaian Kesiapan'
        verbose_name_plural = 'Penilaian Kesiapan'

    @property
    def rata_rata(self):
        return round((self.fisik + self.teknik + self.mental) / 3, 1)

    @property
    def status(self):
        rata = self.rata_rata
        if self.ada_cedera:
            return 'Cedera'
        if rata >= 85:
            return 'Siap Tanding'
        if rata >= 70:
            return 'Siap Latihan'
        if rata >= 50:
            return 'Perlu Pembinaan'
        return 'Belum Siap'

    def __str__(self):
        return f'{self.atlet.nama_lengkap} — {self.tanggal} ({self.rata_rata})'
