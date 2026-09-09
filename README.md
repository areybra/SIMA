<p align="center">
  <img src="https://via.placeholder.com/120x120.png?text=SIMA" alt="SIMA Logo" width="96" height="96" style="border-radius:20px"/>
</p>

<h1 align="center">SIMA — Sistem Interaktif Manajemen Atlet</h1>

<p align="center">
  <strong>Fullstack Django untuk pembinaan atlet yang terstruktur, transparan, dan modern.</strong><br/>
  Root langsung login, 3 role (admin/pelatih/atlet), dark mode, dan tema ungu 60-30-10.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue?style=flat-square" alt="Version"/>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <br/>
  <sub>Template-only (no SPA) • SQLite dev → MySQL prod • Jazzmin Admin (isolated) • 60-30-10 Purple • v0.1.0</sub>
</p>

---

## 📑 Daftar Isi
- [✨ Fitur Utama](#-fitur-utama)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Struktur Project](#-struktur-project)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Environment (.env)](#️-environment-env)
- [🗄️ Database — SQLite / MySQL](#️-database--sqlite--mysql)
- [👥 Role & Hak Akses](#-role--hak-akses)
- [🎨 Tema & Aksesibilitas](#-tema--aksesibilitas)
- [🧪 Verifikasi](#-verifikasi)
- [📄 Dokumen Terkait](#-dokumen-terkait)

---

## ✨ Fitur Utama

| Area | Detail |
|------|--------|
| **Root = Login** | `GET /` redirect ke `/login/` (anon) atau `/dashboard/` (login). Tidak ada halaman publik Tentang/Berita/Prestasi/Kontak — semua dihapus. |
| **Login terisolasi** | `/login/` hanya untuk pelatih & atlet. Admin ditolak dengan pesan generik identik password salah (tidak bocor `/admin/`). Admin hanya via `/admin/` (Jazzmin isolated). |
| **Logo di Login** | Logo perguruan (`perguruan_global`) tampil di halaman login; fallback ikon medal jika belum ada logo. |
| **Dashboard pelatih** | Atlet, kesiapan, prestasi, jadwal/event, dokumen — `strict_role_required('pelatih')` (tanpa celah superuser). Chart tren adaptif dark/light (biru `#2563EB`). |
| **Dashboard atlet** | View-only profil → **jadwal+agenda di bawah profil** → tren (merah `#EF4444`/`#2563EB`/`#22C55E`) → riwayat & dokumen. Plus **Pengaturan Akun sendiri** (username, nama, email, no HP, ganti password). |
| **Dokumen atlet** | Berlabel bebas (KTP/KK/Akta/Ijazah); pelatih kelola semua, atlet dikunci ke profilnya. |
| **Branding global** | `perguruan_global` processor — logo di navbar, footer, sidebar, login. |
| **A11y & Tema** | Skip-link, `:focus-visible`, `prefers-reduced-motion`, favicon SVG data-uri, `theme-color` meta, CSS extracted `static/css/sima.css`. |
| **Keamanan** | Rate limit 5/15 menit (429), upload allowlist 5/10MB, `CSP` + `HSTS` + `Secure` cookies (prod), `SECRET_KEY` wajib acak |

---

## 🛠 Tech Stack

| Lapisan | Teknologi |
|---------|-----------|
| **Fullstack** | Django 5.2 + Django Template (no DRF/SPA) |
| **UI** | Bootstrap 5.3.3, Chart.js 4.4.1, Google Fonts (Outfit + Plus Jakarta Sans + Space Grotesk) |
| **Tema** | 60-30-10 ungu: `#F8FAFC`/`#0B0F19` bg, `#0F172A`/`#F1F5F9` teks, `#7C3AED`/`#A78BFA` aksen |
| **Admin** | `django-jazzmin` 3.0 — isolated hanya `/admin/` |
| **DB** | SQLite (dev) ↔ MySQL/MariaDB (`PyMySQL` + `dj-database-url`) |
| **Lain** | `python-dotenv`, `whitenoise`, `Pillow` + `SecurityHeadersMiddleware` + `ratelimit` cache |

---

## 📁 Struktur Project

```
SIMA/
├── config/              # settings (DB switch), urls (SIMALoginView)
├── apps/
│   ├── accounts/        # CustomUser: admin/pelatih/atlet (jurnalis dihapus), strict decorators, SIMALoginView
│   ├── atlets/          # Cabor, PerguruanProfil, AtletProfile, Prestasi, DokumenAtlet
│   ├── kesiapan/        # PenilaianKesiapan
│   ├── jadwal/          # JadwalLatihan, AgendaEvent
│   └── dashboard/       # router (admin→/admin/) + pelatih/atlet + profil_akun/ganti-password
├── templates/
│   ├── base.html        # {% load static %}, favicon SVG, theme-color, skip-link, <main>
│   ├── registration/login.html  # logo perguruan
│   └── dashboard/       # layout tanpa hamburger, pelatih.html & atlet.html chart adaptif
├── static/css/sima.css  # extracted 60-30-10 + a11y
├── media/ staticfiles/
├── scripts/seed_demo.py
└── manage.py
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/areybra/SIMA.git
cd SIMA
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # default sqlite: kosongkan DATABASE_URL
python manage.py migrate
python manage.py createsuperuser  # atau seed demo
python scripts/seed_demo.py  # admin/admin123, pelatih1/pelatih123, atlet1/atlet123
python manage.py runserver  # → http://127.0.0.1:8000/login/
```

---

## ⚙️ Environment (.env)

| Key | Contoh | Ket |
|-----|--------|-----|
| `SECRET_KEY` | `django-insecure-...` | Generate baru di production |
| `DEBUG` | `True` / `False` | `False` di production |
| `DATABASE_URL` | `mysql://root:pass@localhost:3306/sima` | Prioritas utama |
| `DB_ENGINE` | `sqlite` / `mysql` | Fallback |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Domain production |

---

## 🗄️ Database — SQLite / MySQL

Prioritas: `DATABASE_URL` > `DB_ENGINE`. Kosongkan `DATABASE_URL` untuk dev SQLite.

---

## 👥 Role & Hak Akses (3 Role)

| Fitur | Admin | Pelatih | Atlet |
|-------|:-----:|:-------:|:-----:|
| `/admin/` Jazzmin | ✅ | — | — |
| `/login/` → dashboard | ❌ (ditolak) | ✅ | ✅ |
| Dashboard pelatih (atlet/kesiapan/prestasi/jadwal/dokumen) | ❌ | ✅ | — |
| Dashboard atlet + dokumen sendiri + akun sendiri | — | — | ✅ |
| Cabor & Perguruan (via `/admin/`) | ✅ | — | — |

Strict decorators — superuser tidak lolos ke dashboard.

---

## 🎨 Tema & Aksesibilitas

- **60-30-10 ungu:** bg `#F8FAFC`/`#0B0F19`, teks `#0F172A`/`#F1F5F9`, aksen `#7C3AED`/`#A78BFA`.
- **Chart:** pelatih biru, atlet merah/biru/hijau — grid adaptif, fallback jika kosong.
- **Navbar:** tanpa hamburger (selalu horizontal), footer credit `@areybra`.
- **A11y:** skip-link, focus-visible, reduced-motion, `static/css/sima.css` cacheable.

---

## 🔒 Keamanan

- `SECRET_KEY` wajib env acak saat `DEBUG=False`, `ALLOWED_HOSTS=*` ditolak, `SESSION_COOKIE_AGE=8 jam`, `HSTS`/`NOSNIFF`/`Referrer-Policy` prod.
- Upload allowlist `jpg/jpeg/png/webp` 5MB (foto/logo) & `jpg/png/webp/pdf` 10MB (dokumen), `DATA_UPLOAD_MAX_MEMORY_SIZE=5MB`.
- Rate limit login 5/15 menit/IP+username → 429 (`apps/accounts/ratelimit.py`).
- `SecurityHeadersMiddleware` — `CSP` + `Permissions-Policy` + `X-Content-Type-Options`.

## 🧪 Verifikasi

```bash
python manage.py check
python manage.py shell -c "from django.test import Client; c=Client(); print(c.get('/').status_code, c.get('/login/').status_code)"
# upload php/exe → 200 form error tidak diizinkan ; 6x POST /login/ salah → 429
```

---

## 📄 Dokumen Terkait

- `REQUIREMENT.md` — dependensi & switch DB
- `project.md` — peta URL & model lengkap

<p align="center">
  <sub>© SIMA — 60-30-10 Purple • A11y • Isolated Admin</sub><br/>
  <sub>Developed by <a href="https://github.com/areybra">@areybra</a></sub>
</p>
