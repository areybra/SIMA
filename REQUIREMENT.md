# REQUIREMENT.md — SIMA Dependencies

## Python & Django
- **Python** `>=3.12` (tested 3.12.3 / 3.14.6)
- **Django** `>=5,<6` (`5.2.x`) — fullstack template-only

## Dependencies (requirements.txt)
| Paket | Versi | Kegunaan |
|-------|-------|----------|
| `Django` | `>=5,<6` | Core framework |
| `django-jazzmin` | `3.0.5` | Admin theme `/admin/` isolated |
| `PyMySQL` | `1.2.x` | Driver MySQL/MariaDB (`pymysql.install_as_MySQLdb()`) |
| `dj-database-url` | `3.1.x` | Parse `DATABASE_URL` |
| `python-dotenv` | `1.2.x` | Load `.env` |
| `whitenoise` | `6.12.x` | Serve `staticfiles` + `static/css/sima.css` |
| `Pillow` | `12.x` | Upload `foto`, `logo`, `cover`, `dokumen` |
| `cryptography` | `>=41` | Jazzmin/hash deps |
| *(tanpa paket tambahan)* | — | Rate limit via `LocMemCache`, validasi upload, CSP via middleware lokal |

## System Requirements
- SQLite (default dev) — file `db.sqlite3`, no server
- MySQL 8+ / MariaDB 10+ — via `PyMySQL`
- Node tidak diperlukan (CDN: Bootstrap 5.3.3, Chart.js 4.4.1, Google Fonts)

## Install
```bash
cd SIMA
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # kosongkan DATABASE_URL untuk sqlite
python manage.py migrate
python manage.py createsuperuser  # atau python scripts/seed_demo.py
python manage.py runserver  # → http://127.0.0.1:8000/login/ (pelatih/atlet), /admin/ (admin)
```

## Database Switch (.env)
```
# Prioritas 1
DATABASE_URL=mysql://user:pass@host:3306/sima
# Prioritas 2 (fallback jika DATABASE_URL kosong)
DB_ENGINE=sqlite   # atau mysql + DB_HOST/PORT/NAME/USER/PASSWORD
```

## Keamanan Hardening (v0.1)
- Prod: `SECRET_KEY` wajib, `ALLOWED_HOSTS=*` ditolak, `HSTS`/`NOSNIFF`/`Referrer-Policy`, `Secure` cookies, `SESSION_COOKIE_AGE=8 jam`.
- Upload: allowlist `jpg/jpeg/png/webp` 5MB image, `jpg/png/webp/pdf` 10MB dokumen (`apps/accounts/validators.py`).
- Login: 5 gagal / 15 menit / IP+username → 429 (`apps/accounts/ratelimit.py`).

## Verifikasi
```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py shell -c "from django.test import Client; print(Client().get('/').status_code, Client().get('/login/').status_code)"
# admin POST /login/ → 200 pesan generik identik ; pelatih POST /login/ → 302
# upload .php → 200 form error tidak diizinkan ; 6x salah → 429
```
