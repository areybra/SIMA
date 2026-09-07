<p align="center">
  <img src="https://via.placeholder.com/120x120.png?text=SIMA" alt="SIMA Logo" width="96" height="96" style="border-radius:20px"/>
</p>

<h1 align="center">SIMA — Sistem Interaktif Manajemen Atlet</h1>

<p align="center">
  <strong>Fullstack Django untuk pembinaan atlet yang terstruktur, transparan, dan modern.</strong><br/>
  Kelola biodata, kesiapan (Fisik/Teknik/Mental/VO₂Max), prestasi, jadwal, berita rich-text, dan dokumen — dengan 4 role & dark mode global.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.0.4-blue?style=flat-square" alt="Version"/>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="Postgres"/>
  <img src="https://img.shields.io/badge/MySQL-8%2F8-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <br/>
  <sub>Template-only (no SPA) • SQLite dev → Postgres/MySQL prod • Jazzmin Admin • Mobile-first • v0.0.4 — Supabase pooler fix</sub>
</p>

---

## 📑 Daftar Isi
- [✨ Fitur Utama](#-fitur-utama)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Struktur Project](#-struktur-project)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Environment (.env)](#️-environment-env)
- [🗄️ Database — SQLite / Postgres / MySQL](#️-database--sqlite--postgres--mysql)
- [👥 Role & Hak Akses](#-role--hak-akses)
- [🎨 Dark Mode & Responsive](#-dark-mode--responsive)
- [🧪 Verifikasi](#-verifikasi)
- [📸 Preview](#-preview)
- [📄 Dokumen Terkait](#-dokumen-terkait)

---

## ✨ Fitur Utama

| Area | Detail |
|------|--------|
| **Landing modern** | Hero + KPI (Atlet/Cabor/Prestasi/Jadwal), Berita featured (kategori + views + cover), Tentang/Prestasi ringkas, Kontak teaser — `overflow-wrap:anywhere` anti teks keluar layout |
| **Publik** | `/tentang`, `/berita` (filter kategori/q), `/berita/<slug>` (rich HTML `|safe` + views + terkait), `/prestasi` (filter cabor/tingkat), `/kontak` (form → `ContactMessage` inbox admin) |
| **Berita** | Kategori `umum/latihan/prestasi/event/pengumuman`, **Quill rich text** (heading/bold/italic/list/link/image), `views` auto +1 tiap buka, `is_published/is_featured` |
| **Kontak** | Gantikan Jadwal di landing; jadwal tetap internal di dashboard |
| **Dark mode** | Toggle minimal (track/dot, tanpa ikon berlebihan) di navbar & dashboard top bar; `html.dark` CSS variables; `localStorage:sima-theme` + `prefers-color-scheme`; warna adaptif (tidak tertimpa/invisible) |
| **Auth 4 role** | `admin` (Jazzmin), `pelatih`, `jurnalis`, `atlet` — tanpa registrasi publik; `/admin/` tidak di-link di UI |
| **Dashboard** | **Tanpa navbar** — top bar mobile `d-lg-none sticky-top` + menu **floating offcanvas** (overlay, tidak mendorong konten); desktop `sidebar sticky-top` |
| **Dokumen atlet** | Berlabel bebas (KTP/KK/Akta/Ijazah); admin/pelatih kelola semua, atlet kelola milik sendiri (`atlet` dikunci) |
| **Branding global** | `perguruan_global` context processor — logo tampil di navbar, footer, sidebar, tentang, plus foto atlet di semua list |
| **Jadwal & Kesiapan** | Jadwal mingguan + agenda; penilaian fisik/teknik/mental/VO₂Max/BB/TB/kehadiran/cedera |

---

## 🛠 Tech Stack

| Lapisan | Teknologi |
|---------|-----------|
| **Fullstack** | Django 5.2 + Django Template (no DRF/SPA) |
| **UI** | Bootstrap 5.3.3, Chart.js 4.4.1, Quill 1.3.7, Google Fonts (Outfit + Plus Jakarta Sans + Space Grotesk) |
| **Admin** | `django-jazzmin` 3.0 |
| **DB** | SQLite (dev) ↔ Postgres/Supabase (`psycopg2-binary`) ↔ MySQL/MariaDB (`PyMySQL`) via `DB_ENGINE` |
| **Lain** | `python-dotenv`, `whitenoise`, `Pillow` |

---

## 📁 Struktur Project

```
SIMA/
├── config/              # settings (DB switch), urls, wsgi
├── apps/
│   ├── accounts/        # CustomUser: admin/pelatih/jurnalis/atlet
│   ├── atlets/          # Cabor, PerguruanProfil, AtletProfile, Prestasi, DokumenAtlet
│   ├── kesiapan/        # PenilaianKesiapan
│   ├── jadwal/          # JadwalLatihan, AgendaEvent
│   ├── landing/         # Berita, ContactMessage, context_processors.perguruan
│   └── dashboard/       # router + 3 dashboards + CRUD
├── templates/
│   ├── base.html        # anti-overflow + dark mode + navbar block
│   ├── landing/         # home, tentang, berita_list/detail, prestasi, kontak
│   └── dashboard/       # layout (offcanvas floating) + form-grid
├── static/ media/ staticfiles/
├── scripts/seed_demo.py
├── .env.example         # template env profesional
├── requirements.txt
├── README.md / REQUIREMENT.md / project.md
└── manage.py
```

---

## 🚀 Quick Start

```bash
# 1. Clone & venv
git clone https://github.com/areybra/SIMA.git
cd SIMA
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install
pip install -r requirements.txt

# 3. Env (default sqlite langsung jalan)
cp .env.example .env
# Edit SECRET_KEY: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 4. DB & admin
python manage.py migrate
python manage.py createsuperuser
# atau seed demo (admin/admin123, pelatih1/pelatih123, jurnalis1/jurnalis123, atlet1/atlet123)
python scripts/seed_demo.py

# 5. Run
python manage.py runserver
# → http://127.0.0.1:8000
```

---

## ⚙️ Environment (.env)

| Key | Contoh | Ket |
|-----|--------|-----|
| `SECRET_KEY` | `django-insecure-...` | Generate baru untuk production |
| `DEBUG` | `True` / `False` | `False` di production |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost,example.com` | Domain production |
| `DATABASE_URL` | `postgresql://postgres:pass@thomas.proxy.rlwy.net:24876/sima` | **Otomatis terisi Railway di deploy** — prioritas utama, `DB_ENGINE` diabaikan jika ada |
| `DB_ENGINE` | `sqlite` / `postgres` / `mysql` | Fallback jika `DATABASE_URL` kosong |
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | — | Lihat `.env.example` untuk split mode |
| `DB_SSLMODE` | `require` | Untuk Postgres/Supabase |
| `DB_CONN_MAX_AGE` | `60` | Koneksi persisten |

> **Auto DB di deploy:** `config/settings.py` pakai `_RAILWAY_FALLBACK_URL` jika `DATABASE_URL` tidak di-set & `VERCEL=1` atau `DEBUG=False` — jadi di Vercel/Railway langsung connect ke `thomas.proxy.rlwy.net:24876/sima` tanpa set env manual. Lokal `DEBUG=True` tetap pakai `sqlite` jika `DATABASE_URL` kosong.
> `.env` di-ignore git. `.env.example` sudah berisi `DATABASE_URL` Railway aktif — `cp .env.example .env` langsung jalan untuk dev yang punya akses Railway, atau kosongkan untuk `sqlite`.

---

## 🗄️ Database — SQLite / Postgres / MySQL (via DATABASE_URL)

```env
# Cara 1 — DATABASE_URL (direkomendasikan, otomatis di deploy)
DATABASE_URL=postgresql://postgres:yQoeYmoEyoAIqkoSdmcAPYrqEsdMoytO@thomas.proxy.rlwy.net:24876/sima
# → di Vercel/Railway tidak perlu set manual, sudah fallback otomatis di settings.py
# Supabase contoh: postgresql://postgres.xxx:pass@aws-0-xxx.pooler.supabase.com:6543/postgres?sslmode=require

# Cara 2 — Split (fallback jika DATABASE_URL kosong)
# Dev (tanpa server)
DB_ENGINE=sqlite
# Postgres: DB_ENGINE=postgres + DB_HOST/PORT/NAME/USER/PASSWORD/DB_SSLMODE
# MySQL: DB_ENGINE=mysql + DB_HOST/PORT/NAME/USER/PASSWORD
```

Prioritas: `DATABASE_URL` > `DB_ENGINE`. Deploy Vercel/Railway → `DATABASE_URL` Railway otomatis terpakai (via `_RAILWAY_FALLBACK_URL` di `config/settings.py:110`). Lokal `DEBUG=True` tanpa `DATABASE_URL` → `sqlite`.

---

## 👥 Role & Hak Akses

| Fitur | Admin | Pelatih | Jurnalis | Atlet |
|-------|:-----:|:-------:|:--------:|:-----:|
| `/admin/` (Jazzmin, tidak di-link) | ✅ | — | — | — |
| Dashboard pelatih + atlet/kesiapan/jadwal/cabor/dokumen | ✅ | ✅ | — | — |
| Dashboard jurnalis: berita & prestasi | ✅ | — | ✅ | — |
| Dashboard atlet: data & dokumen sendiri | — | — | — | ✅ |
| Landing publik | ✅ | ✅ | ✅ | ✅ |

Atlet `atlet` dikunci ke `atlet_profile`; jurnalis hanya edit berita miliknya (admin bebas).

---

## 🎨 Dark Mode & Responsive

- **Toggle** minimal track/dot (tanpa emoji) di navbar & dashboard top bar, `html.dark` override variabel (`--paper:#0B1220`, `--surface:#162236`), persist `sima-theme`.
- **Floating offcanvas** `d-lg-none` di dashboard — overlay, tidak mendorong konten; desktop `col-lg-2 sticky-top`.
- **Anti-overflow**: `overflow-wrap:anywhere`, `min-width:0`, `max-width:100%` untuk teks panjang & gambar 1200px.
- **Form** `.form-grid` 2 kolom → 1 kolom <768px.

---

## 🧪 Verifikasi

```bash
python manage.py check
python manage.py shell -c "from django.test import Client; print(Client().get('/').status_code)"
# dark toggle ada?  -> 'themeToggleBtn' in html
# overflow fix ada? -> 'overflow-wrap:anywhere' in base.html
```

---

## 📸 Preview

> Tambahkan screenshot `docs/screenshot-*.png` dan referensikan di sini setelah deploy.

```
docs/
  screenshot-landing.png
  screenshot-dashboard.png
  screenshot-darkmode.png
```

---

## 📄 Dokumen Terkait

- `REQUIREMENT.md` — daftar paket, instalasi, switch DB
- `project.md` — model ringkas & peta URL lengkap
- `templates/` — komentar `overflow-wrap` & `html.dark`

<p align="center">
  <sub>Dibuat untuk pelatih & atlet — pembinaan yang rapi, transparan, dan siap produksi.</sub><br/>
  <sub>© SIMA — Modern • Clear • Spacious • Dark-ready</sub>
</p>
