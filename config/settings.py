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


SECRET_KEY = env('SECRET_KEY', 'django-insecure-sima-dev-key-ganti-di-production')
DEBUG = env_bool('DEBUG', True)
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver').split(',') if h.strip()]

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

# ---- Database: SQLite (dev) <-> Postgres / MySQL (prod) via .env ----
# Postgres/Supabase: DB_ENGINE=postgres (atau supabase) + DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT (6543 untuk pooler)
# MySQL/MariaDB: DB_ENGINE=mysql + DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT (3306)
DB_ENGINE = env('DB_ENGINE', 'sqlite').lower()
if DB_ENGINE in ('postgres', 'postgresql', 'supabase'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', 'postgres'),
            'USER': env('DB_USER', 'postgres'),
            'PASSWORD': env('DB_PASSWORD', ''),
            'HOST': env('DB_HOST', 'localhost'),
            'PORT': env('DB_PORT', '5432'),
            'OPTIONS': {'sslmode': env('DB_SSLMODE', 'require')},
            'CONN_MAX_AGE': int(env('DB_CONN_MAX_AGE', '60') or 60),
        }
    }
elif DB_ENGINE in ('mysql', 'mariadb'):
    try:
        import pymysql  # noqa
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
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
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
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
        'landing.Berita': 'fas fa-newspaper',
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
