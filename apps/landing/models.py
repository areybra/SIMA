from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Berita(models.Model):
    class Kategori(models.TextChoices):
        UMUM = 'umum', 'Umum'
        LATIHAN = 'latihan', 'Latihan'
        PRESTASI = 'prestasi', 'Prestasi'
        EVENT = 'event', 'Event'
        PENGUMUMAN = 'pengumuman', 'Pengumuman'

    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    kategori = models.CharField(max_length=15, choices=Kategori.choices, default=Kategori.UMUM)
    ringkasan = models.CharField(max_length=300, blank=True, help_text='Tampil di kartu & landing (maks 300).')
    konten = models.TextField(help_text='Isi berita — mendukung rich text: heading, bold, italic, list, link, dan gambar.')
    cover = models.ImageField(upload_to='berita/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0, editable=False, help_text='Jumlah dilihat (auto increment saat detail dibuka).')
    is_published = models.BooleanField(default=True, verbose_name='Tampilkan publik')
    is_featured = models.BooleanField(default=False, verbose_name='Featured di landing')
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='berita')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Berita'
        verbose_name_plural = 'Berita'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.judul)[:180]
            slug = base
            i = 1
            while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{i}'
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul


class ContactMessage(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    subjek = models.CharField(max_length=150, blank=True)
    pesan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'

    def __str__(self):
        return f'{self.nama} — {self.subjek or "tanpa subjek"} ({self.created_at:%d/%m/%Y})'
