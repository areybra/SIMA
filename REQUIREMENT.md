# REQUIREMENT.md — SIMA Dependencies

## Python & Django
- **Python** `>=3.12` (tested 3.12.3)
- **Django** `>=5,<6` (`5.2.x`) — fullstack framework + template

## Dependencies (requirements.txt)
| Paket | Versi | Kegunaan Production |
|-------|-------|---------------------|
| `Django` | `>=5,<6` | Core framework |
| `django-jazzmin` | `3.0.5` | Admin theme `/admin/` (modern, tidak di-link publik) |
| `PyMySQL` | `1.2.x` | Driver MySQL/MariaDB (via `DB_ENGINE=mysql`, `pymysql.install_as_MySQLdb()`) |
| `dj-database-url` | `3.1.x` | Parse `DATABASE_URL` untuk MySQL |
| `python-dotenv` | `1.2.x` | Load `.env` untuk `SECRET_KEY`, `ALLOWED_HOSTS`, `DB_*` |
| `whitenoise` | `6.12.x` | Serve `staticfiles` production (CompressedManifest) |
| `Pillow` | `12.x` | Upload `foto`, `logo`, `cover`, `dokumen`, `bukti` (ImageField/FileField) |

## System Requirements
- SQLite (default dev) — tanpa install tambahan, file `db.sqlite3`
- MySQL 8+ / MariaDB 10+ — butuh `PyMySQL`
- Node tidak diperlukan (CDN: Bootstrap 5.3.3, Chart.js 4.4.1, Quill 1.3.7, Google Fonts)

## Install
```bash
cd SIMA
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # atur DB_ENGINE
python manage.py migrate
python manage.py createsuperuser
# atau seed demo
python scripts/seed_demo.py
```

## Database Switch (.env)
```
DB_ENGINE=sqlite   # dev, file db.sqlite3
DB_ENGINE=mysql    # + DB_HOST/PORT/NAME/USER/PASSWORD
```
Lihat `.env.example` untuk contoh lengkap MySQL.

## Verifikasi
```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py shell -c "from django.test import Client; print(Client().get('/').status_code)"
```