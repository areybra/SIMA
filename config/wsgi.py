"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

# Install PyMySQL as MySQLdb BEFORE Django loads the MySQL backend
# This must happen before Django loads the MySQL backend
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()