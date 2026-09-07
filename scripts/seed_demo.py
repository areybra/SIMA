"""Seed demo SIMA: admin, pelatih, atlet + data contoh. Jalankan: .venv/bin/python scripts/seed_demo.py"""
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import django

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.atlets.models import AtletProfile, Cabor, PerguruanProfil, Prestasi
from apps.jadwal.models import AgendaEvent, JadwalLatihan
from apps.kesiapan.models import PenilaianKesiapan


def get_user(username, password, role, **kw):
    u, created = CustomUser.objects.get_or_create(username=username, defaults={'role': role, **kw})
    if created:
        u.set_password(password)
        u.role = role
        if role == 'admin':
            u.is_staff = True
            u.is_superuser = True
        elif role == 'pelatih':
            u.is_staff = True
        u.save()
        print(f'buat user {username}/{password} ({role})')
    else:
        print(f'user {username} sudah ada')
    return u


admin = get_user('admin', 'admin123', 'admin', email='admin@sima.local')
pelatih = get_user('pelatih1', 'pelatih123', 'pelatih')

perguruan, _ = PerguruanProfil.objects.get_or_create(
    id=1,
    defaults={
        'nama': 'Perguruan SIMA Jaya',
        'tentang': 'Perguruan multicabor pembinaan atlet usia dini hingga prestasi.',
        'visi': 'Mencetak atlet berkarakter dan berprestasi nasional.',
        'misi': '1. Latihan rutin terprogram\n2. Pemantauan kesiapan berkala\n3. Kompetisi berjenjang',
        'alamat': 'Jl. Merdeka No. 1',
        'kontak': '0812-0000-0000',
    },
)

cabor_names = ['Pencak Silat', 'Karate', 'Taekwondo', 'Atletik']
cabors = {}
for n in cabor_names:
    c, _ = Cabor.objects.get_or_create(nama=n)
    cabors[n] = c

demo_atlet = [
    ('atlet1', 'atlet123', 'Budi Santoso', 'Pencak Silat', 'Kelas 55kg', 78, 82, 80),
    ('atlet2', 'atlet123', 'Siti Rahma', 'Karate', 'Junior Putri', 85, 88, 90),
    ('atlet3', 'atlet123', 'Andi Pratama', 'Taekwondo', 'Kyorugi U-68', 65, 70, 60),
]
for username, pwd, nama, cabor_nama, kelas, f, t, m in demo_atlet:
    u = get_user(username, pwd, 'atlet')
    profil, _ = AtletProfile.objects.get_or_create(
        nama_lengkap=nama,
        defaults={
            'user': u, 'jenis_kelamin': 'L', 'cabor': cabors[cabor_nama],
            'kelas_kategori': kelas, 'tinggi_cm': 170, 'berat_kg': 62,
            'tahun_masuk': 2023, 'no_hp': '0812-1111-0000',
        },
    )
    if profil.user_id is None:
        profil.user = u
        profil.save()
    for i in range(5):
        tgl = date.today() - timedelta(days=(4 - i) * 7)
        PenilaianKesiapan.objects.get_or_create(
            atlet=profil, tanggal=tgl,
            defaults={
                'fisik': min(100, f + i), 'teknik': min(100, t + i), 'mental': min(100, m + i),
                'vo2max': 42.5 + i * 0.5, 'berat_kg': 62, 'tinggi_cm': 170,
                'kehadiran': 'hadir', 'dinilai_oleh': pelatih,
                'catatan_pelatih': 'Perkembangan baik.',
            },
        )

Prestasi.objects.get_or_create(
    atlet=AtletProfile.objects.get(nama_lengkap='Siti Rahma'),
    nama_kejuaraan='Kejuaraan Provinsi 2025', tingkat='provinsi',
    hasil='Juara 1', tahun=2025,
)

JadwalLatihan.objects.get_or_create(
    hari='Senin', jam_mulai='16:00', jam_selesai='18:00', lokasi='GOR Utama',
    defaults={'pelatih': 'pelatih1', 'kelompok': 'Semua'},
)
JadwalLatihan.objects.get_or_create(
    hari='Rabu', jam_mulai='16:00', jam_selesai='18:00', lokasi='GOR Utama',
    defaults={'pelatih': 'pelatih1', 'kelompok': 'Semua'},
)
AgendaEvent.objects.get_or_create(
    nama='Try Out Antar Dojo', jenis='tryout',
    tanggal_mulai=date.today() + timedelta(days=14),
    defaults={'lokasi': 'GOR Utama', 'deskripsi': 'Uji tanding persiapan kejurprov.'},
)
print('Seed selesai.')
