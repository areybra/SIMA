"""Django settings for SIMA (Sistem Interaktif Manajemen Atlet)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env(key, default=''):
    return os.getenv(key, default)


def env_bool(key, default=False):
    val = os.getenv(key, '')
    if val == '':
        return default
    return val.lower() in ('1', 'true', 'yes', 'on')


DEBUG = env_bool('DEBUG', True)
SECRET_KEY = env('SECRET_KEY', 'django-insecure-sima-dev-key-ganti-di-production')
if not DEBUG and SECRET_KEY.startswith('django-insecure-'):
    raise RuntimeError('SECRET_KEY tidak aman untuk production. Set SECRET_KEY acak di .env')
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver').split(',') if h.strip()]

# --- Vercel / production hardening (fix Bad Request 400) ---
if env('VERCEL') or env('VERCEL_ENV') or env('VERCEL_URL'):
    for h in ['.vercel.app', '.now.sh']:
        if h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)
    vercel_url = env('VERCEL_URL', '').strip()
    if vercel_url and vercel_url not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(vercel_url)
    if not env('ALLOWED_HOSTS'):
        import warnings
        warnings.warn('ALLOWED_HOSTS kosong di Vercel — fallback *.vercel.app aktif. Set ALLOWED_HOSTS eksplisit di dashboard Vercel.')
        ALLOWED_HOSTS.append('.vercel.app')

# CSRF untuk https://*.vercel.app (Vercel selalu https)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in env('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]
if env('VERCEL_URL'):
    _vercel_csrf = f"https://{env('VERCEL_URL').strip()}"
    if _vercel_csrf not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_vercel_csrf)
if env('VERCEL') or env('VERCEL_ENV'):
    for o in ['https://*.vercel.app', 'https://*.now.sh']:
        if o not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(o)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', False)

# --- Hardening: cookies & HSTS (aktif otomatis saat DEBUG=False) ---
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_AGE = 60 * 60 * 8  # 8 jam, was 2 minggu
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS = 'DENY'
else:
    SESSION_COOKIE_AGE = 60 * 60 * 8

DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.atlets',
    'apps.kesiapan',
    'apps.jadwal',
    'apps.dashboard',
    'apps.landing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.accounts.middleware.SecurityHeadersMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.landing.context_processors.perguruan',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---- Database: SQLite (dev) <-> MySQL (prod) via .env ----
# Mendukung 2 cara:
#   1) DATABASE_URL — satu baris URL: mysql://user:pass@host:port/db
#   2) DB_ENGINE + DB_HOST/DB_PORT/... — terpisah (legacy)
# Jika DATABASE_URL diisi, ia diprioritaskan.
# CATATAN: Hanya mendukung MySQL/MariaDB. PostgreSQL TIDAK didukung.
DATABASE_URL = env('DATABASE_URL', '').strip().strip('"').strip("'").strip()

# Gunakan PyMySQL sebagai drop-in replacement untuk mysqlclient (pure Python, no compile)
# mysqlclient butuh build C dengan libmysqlclient yang tidak tersedia di Vercel
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Logika database: DATABASE_URL diprioritaskan, jika kosong pakai DB_ENGINE
if not DEBUG and ALLOWED_HOSTS == ['*']:
    raise RuntimeError('ALLOWED_HOSTS=* tidak diizinkan di production. Set domain eksplisit.')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sima-ratelimit',
    }
}

if not DATABASE_URL:
    DB_ENGINE = env('DB_ENGINE', 'sqlite').lower()
    if DB_ENGINE in ('mysql', 'mariadb'):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': env('DB_NAME', 'sima'),
                'USER': env('DB_USER', 'root'),
                'PASSWORD': env('DB_PASSWORD', ''),
                'HOST': env('DB_HOST', 'localhost'),
                'PORT': env('DB_PORT', '3306'),
                'OPTIONS': {'charset': 'utf8mb4'},
                'CONN_MAX_AGE': int(env('DB_CONN_MAX_AGE', '60') or 60),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Reject PostgreSQL URLs explicitly
    if DATABASE_URL.strip().lower().startswith(('postgres://', 'postgresql://')):
        raise ImproperlyConfigured(
            "PostgreSQL tidak didukung. Gunakan MySQL/MariaDB URL (mysql://...). "
        )
    # Coba pakai dj-database-url jika tersedia, fallback ke parsing manual
    try:
        import dj_database_url  # type: ignore
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=int(env('DB_CONN_MAX_AGE', '60') or 60),
                ssl_require=False,
            )
        }
        # MySQL butuh charset utf8mb4
        if DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            opts = DATABASES['default'].setdefault('OPTIONS', {})
            if 'charset' not in opts:
                opts['charset'] = 'utf8mb4'
    except ImportError:
        # Fallback manual parsing tanpa dj-database-url
        from urllib.parse import parse_qs, unquote, urlparse

        _url = urlparse(DATABASE_URL)
        _scheme = _url.scheme.lower()
        _qs = parse_qs(_url.query)
        if _scheme in ('mysql', 'mysql2', 'mariadb'):
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': unquote(_url.path.lstrip('/')) or env('DB_NAME', 'sima'),
                    'USER': unquote(_url.username or 'root'),
                    'PASSWORD': unquote(_url.password or ''),
                    'HOST': _url.hostname or 'localhost',
                    'PORT': str(_url.port or 3306),
                    'OPTIONS': {'charset': 'utf8mb4'},
                    'CONN_MAX_AGE': int(env('DB_CONN_MAX_AGE', '60') or 60),
                }
            }
        else:
            # fallback sqlite jika scheme tidak dikenali
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard-router'
LOGOUT_REDIRECT_URL = 'landing'

# ---- django-jazzmin ----
JAZZMIN_SETTINGS = {
    'site_title': 'SIMA Admin',
    'site_header': 'SIMA',
    'site_brand': 'SIMA',
    'welcome_sign': 'Sistem Interaktif Manajemen Atlet',
    'copyright': 'SIMA Perguruan',
    'show_sidebar': True,
    'navigation_expanded': True,
    'topmenu_links': [
        {'name': 'Lihat Situs', 'url': '/', 'new_window': True},
    ],
    'icons': {
        'accounts.CustomUser': 'fas fa-users-cog',
        'atlets.AtletProfile': 'fas fa-running',
        'atlets.Cabor': 'fas fa-medal',
        'atlets.Prestasi': 'fas fa-trophy',
        'atlets.PerguruanProfil': 'fas fa-school',
        'atlets.DokumenAtlet': 'fas fa-folder-open',
        'kesiapan.PenilaianKesiapan': 'fas fa-heartbeat',
        'jadwal.JadwalLatihan': 'fas fa-calendar-alt',
        'landing.ContactMessage': 'fas fa-envelope',
        'jadwal.AgendaEvent': 'fas fa-flag',
    },
    'order_with_respect_to': ['accounts', 'atlets', 'kesiapan', 'jadwal'],
}
JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': 'navbar-primary',
    'accent': 'accent-primary',
    'navbar': 'navbar-dark',
    'no_navbar_border': False,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': True,
    'theme': 'default',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}