# SIMA — Sistem Interaktif Manajemen Atlet

## 1. Informasi Project

**SIMA** adalah aplikasi web fullstack untuk mengolah data para atlet beserta tingkat kesiapannya hingga jadwal rutin latihan.

- **Pengguna utama 1 — Pelatih:** mengolah data atlet, menginput penilaian kesiapan rutin, mencatat prestasi, serta mengatur jadwal & dokumen atlet, agenda/event. Akses via `/login/` → `/dashboard/pelatih/`.
- **Pengguna utama 2 — Atlet/Anggota:** memantau data tentang dirinya sendiri (profil, tren kesiapan, prestasi, jadwal) dalam mode **view-only**, plus **upload dokumen sendiri** (KTP/KK/Akta/Ijazah dll dengan label bebas) dan **pengaturan akun sendiri** (username, nama, email, no HP, ganti password). Jadwal & agenda kini tampil tepat di bawah profil.
- **Pengguna ke-3 — Admin:** mengelola seluruh data via **Jazzmin `/admin/` saja** — terisolasi penuh dari dashboard. Tidak dapat login di `/login/` (ditolak dengan pesan generik tersamarkan) dan tidak dapat membuka `/dashboard/*` (403). Buat akun pelatih/atlet via `/admin/`.
- **Tanpa registrasi publik.** Semua akun dibuat oleh admin. Landing publik dihapus — `GET /` langsung redirect ke `/login/` (anon) atau `/dashboard/` (login). Tidak ada halaman Tentang/Berita/Prestasi/Kontak publik lagi.

## 2. Tujuan

 1. Mendigitalkan biodata atlet (termasuk TB/BB), kategori/kelas, dan status aktif.
 2. Memantau kesiapan atlet secara berkala: fisik, teknik, mental (0–100), VO2Max, snapshot BB/TB, kehadiran, status cedera, dan catatan pelatih. Chart menggunakan warna grafik umum (merah Fisik, biru Teknik, hijau Mental) + adaptif light/dark.
 3. Menyajikan statistik: tren kesiapan, top atlet, distribusi kehadiran, daftar cedera, dan prestasi terbaru — hanya di dashboard (landing dihapus).
 4. Mengelola jadwal latihan rutin mingguan dan agenda/event (try out, kejuaraan, latihan gabungan) — tampil di dashboard pelatih dan tepat di bawah profil atlet.
 5. Memberi atlet akses transparan dan terbatas hanya pada datanya sendiri, termasuk kelola dokumen pribadi berlabel dan pengaturan akun login sendiri.
 6. Isolasi keamanan: admin hanya via `/admin/`; pelatih dan atlet hanya via `/login/` → `/dashboard/`.

## 3. Tech Stack

| Lapisan   | Teknologi |
|-----------|-----------|
| Fullstack | Django 5.x + Django Template (tanpa SPA/DRF) |
| UI publik & dashboard | Bootstrap 5.3.3 (CDN) + design tokens 60-30-10 ungu |
| Grafik    | Chart.js 4 (CDN) — warna merah/hijau/biru standar, grid adaptif dark |
| Desain    | 60-30-10: Light bg `#F8FAFC` / Dark bg `#0B0F19`, teks `#0F172A` / `#F1F5F9`, aksen `#7C3AED` / `#A78BFA` (neon) |
| Admin theme | `django-jazzmin` 3.0 — hanya untuk `/admin/` (isolated) |
| Database dev | SQLite (`db.sqlite3`) |
| Database prod | MySQL/MariaDB via `PyMySQL` (switch lewat `.env` + `DATABASE_URL`) |
| Config    | `python-dotenv` (`.env` / `.env.example`) |
| Static prod | `whitenoise` + `static/css/sima.css` (extracted) |
| Media upload | Pillow (`media/atlet/`, `media/prestasi/`, `media/perguruan/`, `media/dokumen/`) |
| A11y | skip-link, `:focus-visible`, `prefers-reduced-motion`, favicon SVG, manifest, meta theme-color |
| Zona waktu | Asia/Jakarta, bahasa `id` |
| Keamanan  | `/admin/` isolated; pesan login admin disamarkan identik password salah; admin ditolak di `/login/` dan `/dashboard/*`; rate limit 5/15 menit; upload allowlist + 5/10MB; CSP + HSTS + Secure cookies (prod) |

## 4. Peran & Hak Akses (3 Role Aktif)

| Fitur | Admin (`/admin/`) | Pelatih | Atlet |
|-------|:-----------------:|:-------:|:-----:|
| `/admin/` Jazzmin (CRUD semua model) | ✅ | ❌ | ❌ |
| `/login/` → `/dashboard/` | ❌ (ditolak, pesan generik) | ✅ | ✅ |
| Dashboard pelatih: atlet/kesiapan/prestasi/jadwal/dokumen | ❌ (403) | ✅ | ❌ |
| Dashboard atlet `/dashboard/saya/` + dokumen sendiri + pengaturan akun | ❌ | ❌ | ✅ |
| Pengaturan akun `/dashboard/akun/` (username, nama, email, no HP, ganti password) | ❌ (403) | ✅ | ✅ |
| Cabor & Profil Perguruan (hanya via `/admin/`) | ✅ | ❌ | ❌ |
| Logo perguruan di halaman login (via `perguruan_global`) | — | — | — |
| Registrasi publik | ❌ | ❌ | ❌ |

Proteksi: `apps/accounts/decorators.py` (`strict_role_required`, `pelatih_required`, `atlet_required` — **tanpa** pengecualian superuser); `SIMALoginView` menolak admin dengan pesan `invalid_login` generik; dashboard `profil_akun` & `GantiPasswordView` dikunci untuk pelatih/atlet saja.

## 5. Struktur Project

```
SIMA/
├── manage.py
├── requirements.txt
├── .env / .env.example      # DATABASE_URL > DB_ENGINE fallback
├── db.sqlite3               # dev saja
├── config/
│   ├── settings.py          # custom user, jazzmin, DB env, static/media, login URLs
│   └── urls.py              # admin, login/logout, dashboard/, landing (hanya /)
├── apps/
│   ├── accounts/            # CustomUser(role: admin/pelatih/atlet), decorators strict, SIMALoginView, forms AccountProfileForm
│   ├── atlets/              # Cabor, PerguruanProfil, AtletProfile, Prestasi, DokumenAtlet
│   ├── kesiapan/            # PenilaianKesiapan
│   ├── jadwal/              # JadwalLatihan, AgendaEvent
│   ├── dashboard/           # router + pelatih/atlet dashboards + CRUD + profil_akun/ganti-password
│   └── landing/             # hanya redirect / (ContactMessage masih ada, Berita dihapus)
├── templates/
│   ├── base.html            # {% load static %}, favicon SVG data-uri, theme-color, skip-link, <main id=main-content>, static/css/sima.css
│   ├── registration/login.html  # logo perguruan di atas form + pesan generik tersamarkan
│   └── dashboard/           # layout tanpa hamburger, profil_akun.html, ganti_password.html, atlet.html (jadwal di bawah profil), pelatih.html (chart adaptif)
├── static/css/sima.css      # extracted design tokens 60-30-10 + a11y
├── static/ / staticfiles/ / media/
└── scripts/seed_demo.py     # akun admin/pelatih/atlet + data contoh
```

## 6. Model Data (ringkas)

- **CustomUser** — `username, password, role(admin/pelatih/atlet), first_name, last_name, email, no_hp`. Role `jurnalis` dihapus (migrasi `0003`).
- **Cabor** — master cabang olahraga (hanya via `/admin/`).
- **PerguruanProfil** — singleton profil perguruan (nama, tentang, visi, misi, alamat, kontak, logo) — hanya via `/admin/`, tampil di login & footer.
- **AtletProfile** — `user(OneToOne, opsional)`, nama, JK, TTL, cabor FK, kelas/kategori, tahun masuk, `tinggi_cm`, `berat_kg`, status aktif, foto, kontak.
- **Prestasi** — atlet FK, kejuaraan, tingkat, hasil, tahun, bukti.
- **PenilaianKesiapan** — atlet FK + tanggal (unik), fisik/teknik/mental 0–100, `vo2max`, snapshot BB/TB, kehadiran, `ada_cedera` + keterangan, catatan pelatih, `dinilai_oleh`.
- **JadwalLatihan** — cabor FK (kosong = umum), hari, jam mulai–selesai, lokasi, pelatih, kelompok, aktif.
- **AgendaEvent** — nama, jenis, tanggal mulai–selesai, lokasi, cabor, deskripsi.
- **ContactMessage** — masih ada (inbox), namun halaman publik `/kontak/` sudah dihapus. Dikelola via `/admin/`.
- **Berita** — **dihapus total** (migrasi `landing/0003_delete_berita`).
- **DokumenAtlet** — `atlet FK, label, file, keterangan, uploaded_by FK, created_at`. Atlet dikunci ke profilnya.

## 7. Peta URL (saat ini)

```
GET  /                                  redirect → /login/ (anon) / /dashboard/ (login)
GET  /login/  POST /logout/             auth pelatih/atlet only (admin ditolak, pesan generik)
GET  /admin/                            Jazzmin — hanya admin (isolated)
GET  /dashboard/                        router: admin→/admin/, pelatih→pelatih, atlet→saya
GET  /dashboard/pelatih/                overview pelatih (chart tren adaptif dark/light, fallback jika kosong)
GET  /dashboard/saya/                   dashboard atlet (profil → jadwal+agenda → tren → riwayat/dokumen+prestasi)
GET  /dashboard/akun/  +  /dashboard/akun/ganti-password/   pengaturan akun sendiri (pelatih/atlet only)
CRUD /dashboard/pelatih/atlet/...       pelatih only (strict)
CRUD /dashboard/pelatih/kesiapan/...
CRUD /dashboard/pelatih/prestasi/...
CRUD /dashboard/pelatih/jadwal/... + event/...
CRUD /dashboard/pelatih/dokumen/...     pelatih only
CRUD /dashboard/saya/dokumen/...        atlet only (atlet dikunci)
# Dihapus: /tentang/, /berita/*, /prestasi/, /kontak/, /dashboard/jurnalis/*, /dashboard/pelatih/cabor/, /dashboard/pelatih/profil-perguruan/, /dashboard/pelatih/pengguna/* (semua via /admin/), /dashboard/pelatih/berita/* (Berita dihapus)
```

## 8. Cara Menjalankan (dev)

```bash
cd SIMA
.venv\Scripts\python -m pip install -r requirements.txt
cp .env.example .env            # default SQLite: DATABASE_URL= kosong + DB_ENGINE=sqlite
.venv\Scripts\python manage.py migrate
.venv\Scripts\python scripts/seed_demo.py   # akun: admin/admin123, pelatih1/pelatih123, atlet1/atlet123
.venv\Scripts\python manage.py runserver
# → http://127.0.0.1:8000/login/   (pelatih/atlet)
# → http://127.0.0.1:8000/admin/   (admin)
```

## 9. Migrasi ke MySQL

1. Siapkan DB MySQL/MariaDB.
2. Isi `.env`: `DATABASE_URL=mysql://user:pass@host:3306/sima` (prioritas) atau `DB_ENGINE=mysql` + split vars.
3. `python manage.py migrate` (+ `createsuperuser` bila DB kosong).

## 10. Protokol Check & Test (wajib tiap pembaruan)

```bash
.venv\Scripts\python manage.py check
.venv\Scripts\python manage.py shell -c "from django.test import Client; c=Client(); print(c.get('/').status_code, c.get('/login/').status_code)"
# admin POST /login/ → 200 (pesan identik salah, anonim) ; pelatih POST /login/ → 302 → /dashboard/
# admin /admin/ 200 ; admin /dashboard/* 403 ; pelatih /dashboard/pelatih/ 200 ; atlet /dashboard/saya/ 200
```

## 11. Desain — 60-30-10 Ungu + A11y + Chart Umum

- **60% `#F8FAFC` (light) / `#0B0F19` (dark):** background paper — bersih & premium.
- **30% `#0F172A` / `#F1F5F9`:** teks & komponen — kontras tajam, nyaman di gelap.
- **10% `#7C3AED` / `#A78BFA`:** aksen ungu vivid/neon untuk CTA & highlight — tetap nyala di dark.
- **Chart:** garis Tunggal biru `#2563EB` (pelatih) dan trio merah `#EF4444` / biru `#2563EB` / hijau `#22C55E` (atlet), grid adaptif `#E6E9EF` ↔ `#1E2F4A`, fallback teks jika data kosong.
- **Layout:** CSS extracted ke `static/css/sima.css` (cacheable via Whitenoise), skip-link, `:focus-visible`, `prefers-reduced-motion`, favicon SVG inline, `theme-color` meta.
- **Navbar:** tanpa hamburger (selalu horizontal, `d-flex`), footer credit `@areybra`.

## 12. Keamanan — Hardening v0.1

- **Settings prod:** `SECRET_KEY` wajib acak saat `DEBUG=False` (gagal boot jika `django-insecure`), `ALLOWED_HOSTS=*` ditolak, `SESSION_COOKIE_AGE=8 jam`, `Secure`/`HttpOnly`/`SameSite=Lax` + `HSTS 1 tahun + preload + NOSNIFF + Referrer-Policy` aktif otomatis saat prod; `CACHES LocMemCache` untuk rate limit.
- **Upload:** `apps/accounts/validators.py` — allowlist `jpg/jpeg/png/webp` (foto/logo, 5MB) dan `jpg/png/webp/pdf` (dokumen/bukti, 10MB); `apps/atlets/forms.py` clean_* memblokir `.php/.exe/.svg` dkk.
- **Brute-force:** `apps/accounts/ratelimit.py` 5 gagal / 15 menit per `IP+username` → `429`; `SIMALoginView` bump/clear cache, pesan tetap generik.
- **Headers:** `apps/accounts/middleware.py:SecurityHeadersMiddleware` — `CSP` (`self` + `cdn.jsdelivr.net` + `fonts.googleapis`), `Permissions-Policy`, `Referrer-Policy`, `X-Content-Type-Options`.
