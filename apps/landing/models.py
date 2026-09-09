from django.db import models


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
