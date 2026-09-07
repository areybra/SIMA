# SIMA — Sistem Interaktif Manajemen Atlet

Fullstack Django (template) untuk mengelola data atlet, kesiapan, prestasi, jadwal, berita, dan dokumen.

## Fitur Utama
- **Landing** modern non-klasik: hero, KPI, berita featured (kategori + views + cover), tentang/visi, prestasi top, kontak teaser — **tidak ada teks keluar layout** (`overflow-wrap: anywhere`, `max-width:100%`, `min-width:0` di `base.html`)
- **Tentang / Berita / Prestasi / Kontak** publik — Berita pakai **kategori** (umum/latihan/prestasi/event/pengumuman), **rich text** Quill (heading/bold/italic/list/link/image → HTML `|safe`), **views** auto +1 tiap buka detail
- **Kontak** publik gantikan **Jadwal** di landing — form `nama/email/subjek/pesan` → `ContactMessage` (admin/jazzmin inbox); jadwal tetap internal di dashboard
- **Dark mode** global — toggle 🌙/☀️ di navbar (publik) & top bar dashboard, `html.dark` CSS variables, persist `localStorage:sima-theme`, hormati `prefers-color-scheme`, anti-FOUC via inline script di `<head>`
- **Auth 4 role** — `admin` (superuser), `pelatih`, `jurnalis`, `atlet` (`CustomUser.role`), tanpa registrasi publik; `/admin/` (Jazzmin) tidak di-link di UI (akses langsung)
- **Dashboard tanpa navbar** — top bar `d-lg-none sticky-top` pengganti navbar di mobile, menu **floating offcanvas** (`#dashOffcanvas` `offcanvas-start`) overlay, tidak mendorong konten; desktop sidebar `col-lg-2 d-none d-lg-block sticky-top`
- **Atlet**: view-only + upload **dokumen berlabel** (KTP/KK/Akta/Ijazah bebas); foto profil tampil di `atlet_list`, `penilaian`, `prestasi`, `dokumen`, dashboard
- **Jurnalis**: CRUD **berita** (rich text + kategori + views) & **prestasi**; `views` tampil di list/detail
- **Pelatih**: CRUD atlet, **kesiapan** (fisik/teknik/mental/VO2Max/BB/TB/kehadiran/cedera), prestasi, jadwal/event, dokumen, cabor, profil perguruan
- **Logo perguruan** global via `context_processor` (`perguruan_global`) — navbar, footer, sidebar, tentang
- **Footer full-bleed** (`width:100vw; margin-left:calc(50% - 50vw)`)

## Tech Stack
- Django 5.x + Template, Bootstrap 5.3.3, Chart.js 4.4.1, Quill 1.3.7, Google Fonts (Outfit + Plus Jakarta Sans + Space Grotesk)
- DB: **SQLite** (dev) ↔ **Postgres/Supabase** (`psycopg2-binary`) ↔ **MySQL/MariaDB** (`PyMySQL`) via `.env:DB_ENGINE`
- `python-dotenv`, `whitenoise`, `Pillow`

## Struktur Penting
```
config/settings.py  # DB switch sqlite/postgres/mysql, jazzmin, static/media
apps/accounts       # CustomUser (admin/pelatih/jurnalis/atlet)
apps/atlets         # Cabor, PerguruanProfil, AtletProfile, Prestasi, DokumenAtlet
apps/kesiapan       # PenilaianKesiapan
apps/jadwal         # JadwalLatihan, AgendaEvent
apps/landing        # Berita (kategori/views/richtext), ContactMessage, context_processor perguruan
apps/dashboard      # router + 3 dashboards + CRUD
templates/base.html # overflow fix + dark mode + navbar block + offcanvas
templates/landing/* # home, tentang, berita_list/detail (rich-content), prestasi, kontak
templates/dashboard/layout.html # top bar mobile + offcanvas floating + desktop sidebar
```

## Quick Start
```bash
cd SIMA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # default DB_ENGINE=sqlite langsung jalan
python manage.py migrate
python manage.py createsuperuser  # atau python scripts/seed_demo.py
python manage.py runserver
# akun demo seed: admin/admin123, pelatih1/pelatih123, jurnalis1/jurnalis123, atlet1/atlet123
```

## Environment (.env)
```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
DB_ENGINE=sqlite  # sqlite | postgres | mysql
# postgres: DB_HOST/PORT(5432/6543 pooler)/NAME/USER/PASSWORD/DB_SSLMODE
# mysql: DB_HOST/PORT(3306)/NAME/USER/PASSWORD
```

## Dark Mode
- Toggle di navbar publik & dashboard top bar (🌙/☀️)
- `html.dark` override CSS variables (`--paper:#0B1220`, `--surface:#162236`, etc.)
- Persist `localStorage:sima-theme`, fallback `prefers-color-scheme`
- Semua halaman terpengaruh (base variables dipakai nav/card/table/form/footer)

## Catatan Layout
- `base.html` pakai `overflow-wrap:anywhere; word-break:break-word; min-width:0` untuk cegah teks panjang keluar card/grid
- `berita_detail.html` pakai `.rich-content` (`|safe`) dengan style `h1-3, img, blockquote, a`
- Dashboard `form.html` pakai `.form-grid` 2 kolom (1 kolom <768px) agar tidak memanjang

Lihat `REQUIREMENT.md` untuk daftar paket & `project.md` untuk detail model/URL.
