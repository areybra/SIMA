from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        PELATIH = 'pelatih', 'Pelatih'
        ATLET = 'atlet', 'Atlet/Anggota'
        JURNALIS = 'jurnalis', 'Jurnalis'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.ATLET)
    no_hp = models.CharField(max_length=20, blank=True)

    @property
    def is_admin_role(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    @property
    def is_pelatih(self):
        return self.role == self.Roles.PELATIH or self.is_admin_role

    @property
    def is_atlet(self):
        return self.role == self.Roles.ATLET

    @property
    def is_jurnalis(self):
        return self.role == self.Roles.JURNALIS or self.is_admin_role

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
