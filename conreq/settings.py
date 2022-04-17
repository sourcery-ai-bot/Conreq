"""
Django settings for Conreq project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import json
import os
import secrets
import sys
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from tzlocal import get_localzone_name

from conreq.utils.environment import (
    get_base_url,
    get_bool_from_env,
    get_database_type,
    get_debug,
    get_str_from_env,
    set_env,
)
from conreq.utils.generic import list_modules

# Project Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(BASE_DIR, "conreq", "core")
DATA_DIR = get_str_from_env("DATA_DIR", os.path.join(BASE_DIR, "data"), dot_env=False)
APPS_DIR = os.path.join(DATA_DIR, "packages")
MEDIA_DIR = os.path.join(DATA_DIR, "media")
BACKUP_DIR = os.path.join(DATA_DIR, "backup")
TEMP_DIR = os.path.join(DATA_DIR, "temp")
USER_STATICFILES_DIR = os.path.join(DATA_DIR, "static")
LOG_DIR = os.path.join(DATA_DIR, "logs")
METRICS_DIR = os.path.join(DATA_DIR, "metrics")
MAKE_DIRS = [
    DATA_DIR,
    APPS_DIR,
    MEDIA_DIR,
    BACKUP_DIR,
    TEMP_DIR,
    USER_STATICFILES_DIR,
    LOG_DIR,
    METRICS_DIR,
]
for directory in MAKE_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)


# Environment Variables
DOTENV_FILE = os.path.join(DATA_DIR, "settings.env")
os.environ["CONREQ_DOTENV_FILE"] = DOTENV_FILE
if not os.path.exists(DOTENV_FILE):
    with open(DOTENV_FILE, "w", encoding="utf-8") as fp:
        pass
DEBUG = get_debug()
DB_ENGINE = get_database_type()
MYSQL_CONFIG_FILE = get_str_from_env("MYSQL_CONFIG_FILE", "")
SSL_SECURITY = get_bool_from_env("SSL_SECURITY", False)
PWNED_VALIDATOR = get_bool_from_env("PWNED_VALIDATOR", True)
X_FRAME_OPTIONS = get_str_from_env("X_FRAME_OPTIONS", "DENY")
BASE_URL = get_base_url()


# Basic Configuration
with (Path(BASE_DIR) / ".version").open() as f:
    CONREQ_VERSION = f.read().strip()


# Python Packages
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
# SILKY_ANALYZE_QUERIES = True # Broken with Django 3.2
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = METRICS_DIR
HTML_MINIFY = True
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
COMPRESS_OUTPUT_DIR = "minified"
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = "compressor.storage.BrotliCompressorFileStorage"
COMPRESS_FILTERS = {
    "css": ["compressor.filters.cssmin.rCSSMinFilter"],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
HUEY_FILENAME = os.path.join(DATA_DIR, "bg_tasks.sqlite3")
HUEY = {
    "name": "huey",  # DB name for huey.
    "huey_class": "huey.SqliteHuey",  # Huey implementation to use.
    "filename": HUEY_FILENAME,  # Sqlite filename
    "results": True,  # Store return values of tasks.
    "immediate": False,  # If True, run tasks synchronously.
    "strict_fifo": True,  # Utilize Sqlite AUTOINCREMENT to have unique task IDs
    "consumer": {
        "workers": 20,
    },
}


# Email Settings
if (
    get_str_from_env("EMAIL_HOST")
    and get_str_from_env("EMAIL_PORT")
    and get_str_from_env("EMAIL_HOST_USER")
    and get_str_from_env("EMAIL_HOST_PASSWORD")
):
    EMAIL_ENABLED = True
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = get_bool_from_env("EMAIL_USE_TLS", True)
    EMAIL_HOST = get_str_from_env("EMAIL_HOST")
    EMAIL_PORT = get_str_from_env("EMAIL_PORT")
    EMAIL_HOST_USER = get_str_from_env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_str_from_env("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_ENABLED = False


# PWA
PWA_APP_NAME = get_str_from_env("APP_NAME", "Conreq")
PWA_APP_DESCRIPTION = get_str_from_env("APP_DESCRIPTION", "Content Requesting")
PWA_APP_THEME_COLOR = "#3fcfa6"
PWA_APP_BACKGROUND_COLOR = "#04110d"
PWA_APP_ICONS = [
    {
        "src": BASE_URL + "/static/icons/standard.png",
        "sizes": "512x512",
        "purpose": "any",
    },
    {
        "src": BASE_URL + "/static/icons/maskable.png",
        "sizes": "512x512",
        "purpose": "maskable",
    },
]
PWA_APP_ICONS_APPLE = [
    {"src": BASE_URL + "/static/icons/apple-touch-icon.png", "sizes": "180x180"}
]
PWA_APP_SPLASH_SCREEN = []
PWA_APP_START_URL = BASE_URL + "/"
PWA_APP_SCOPE = PWA_APP_START_URL
PWA_APP_DEBUG_MODE = DEBUG


# Logging
CONREQ_LOG_FILE = os.path.join(LOG_DIR, "conreq.log")
ACCESS_LOG_FILE = os.path.join(LOG_DIR, "access.log")
if DEBUG:
    LOG_LEVEL = get_str_from_env("LOG_LEVEL", "INFO")
else:
    LOG_LEVEL = get_str_from_env("LOG_LEVEL", "WARNING")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
        },
        "minimal": {
            "format": "%(levelname)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "minimal",
        },
        "conreq_logs": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "main",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "encoding": "utf-8",
            "filename": CONREQ_LOG_FILE,
        },
    },
    "loggers": {
        "django": {
            "level": LOG_LEVEL,
        },
        "hypercorn": {
            "level": LOG_LEVEL,
        },
        "conreq": {
            "level": LOG_LEVEL,
        },
        "huey": {
            "level": LOG_LEVEL,
        },
    },
}
for logger in LOGGING["loggers"]:
    LOGGING["loggers"][logger]["handlers"] = ["console", "conreq_logs"]


# Security Settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
ALLOWED_HOSTS = [
    host.strip() for host in get_str_from_env("ALLOWED_HOSTS", "*").split(",")
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in get_str_from_env("TRUSTED_ORIGINS", "").split(",")
    if origin
]
if SSL_SECURITY:
    SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
    SECURE_HSTS_PRELOAD = True  # Allow for HSTS preload
    SECURE_HSTS_SECONDS = 31536000  # Allow for HSTS preload
    SESSION_COOKIE_SECURE = True  # Only send cookie over HTTPS
    CSRF_COOKIE_SECURE = True  # Only send cookie over HTTPS
    LANGUAGE_COOKIE_SECURE = True  # Only send cookie over HTTPS
    LANGUAGE_COOKIE_HTTPONLY = True  # Do not allow JS to access cookie


# API Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "conreq.core.api.permissions.HasAPIKey",
    ],
}


# settings.json (old) -> settings.env
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r+", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)
        if settings.get("DB_ENCRYPTION_KEY"):
            set_env("DB_ENCRYPTION_KEY", settings["DB_ENCRYPTION_KEY"])
        if settings.get("SECRET_KEY"):
            set_env("WEB_ENCRYPTION_KEY", settings["SECRET_KEY"])
    os.remove(SETTINGS_FILE)


# Encryption
if get_str_from_env("DB_ENCRYPTION_KEY"):
    FIELD_ENCRYPTION_KEYS = [get_str_from_env("DB_ENCRYPTION_KEY")]
else:
    FIELD_ENCRYPTION_KEYS = [secrets.token_hex(32)]
    set_env("DB_ENCRYPTION_KEY", FIELD_ENCRYPTION_KEYS[0])
if get_str_from_env("WEB_ENCRYPTION_KEY"):
    SECRET_KEY = get_str_from_env("WEB_ENCRYPTION_KEY")
else:
    SECRET_KEY = set_env("WEB_ENCRYPTION_KEY", get_random_secret_key())[1]


# Django Apps & Middleware
sys.path.append(APPS_DIR)  # User Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *list_modules(CORE_DIR, prefix="conreq.core."),
    "channels",  # Websocket library
    "encrypted_fields",  # Allow for encrypted text in the DB
    "solo",  # Allow for single-row fields in the DB
    "django_cleanup.apps.CleanupConfig",  # Automatically delete old image files
    "huey.contrib.djhuey",  # Queuing background tasks
    "compressor",  # Minifies CSS/JS files
    "url_or_relative_url_field",  # Validates relative URLs
    "rest_framework",  # OpenAPI Framework
    "rest_framework_api_key",  # API Key Manager
    "rest_framework.authtoken",  # API User Authentication
    *list_modules(APPS_DIR),  # User Installed Apps
]
MIDDLEWARE = [
    "compression_middleware.middleware.CompressionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files through Django securely
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",  # Compresses HTML files
    "htmlmin.middleware.MarkRequestMiddleware",  # Marks the request as minified
]


# Enabling apps/middleware based on flags
if X_FRAME_OPTIONS.lower() != "false" and not DEBUG:
    # Block embedding conreq
    MIDDLEWARE.append("django.middleware.clickjacking.XFrameOptionsMiddleware")
if DEBUG:
    # Performance analysis tools
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
    # API docs generator
    INSTALLED_APPS.append("drf_yasg")


# URL Routing and Page Rendering
ROOT_URLCONF = "conreq.urls"
ASGI_APPLICATION = "conreq.asgi.application"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Databases
if DB_ENGINE == "MYSQL":
    if not MYSQL_CONFIG_FILE:
        print("MYSQL_CONFIG_FILE is not set!")
        sys.exit(1)
    elif not os.path.exists(MYSQL_CONFIG_FILE):
        print(f"MYSQL_CONFIG_FILE '{MYSQL_CONFIG_FILE}' does not exist!")
        sys.exit(1)
    else:
        import pymysql

        pymysql.install_as_MySQLdb()

        # MySQL
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "OPTIONS": {
                    "read_default_file": MYSQL_CONFIG_FILE,
                },
            }
        }
else:
    # SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(DATA_DIR, "db.sqlite3"),
            "OPTIONS": {
                "timeout": 3,  # 3 second query timeout
            },
        }
    }
CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": os.path.join(DATA_DIR, "cache"),
        "TIMEOUT": 300,  # Django setting for default timeout of each key.
        "SHARDS": 8,  # Number of "sharded" cache dbs to create
        "DATABASE_TIMEOUT": 0.25,  # 250 milliseconds
        "OPTIONS": {"size_limit": 2 ** 30},  # 1 gigabyte
    }
}


# User Authentication
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LOGIN_REDIRECT_URL = "base:landing"
LOGIN_URL = "sign_in"
if PWNED_VALIDATOR:
    AUTH_PASSWORD_VALIDATORS.append(
        {
            "NAME": "pwned_passwords_django.validators.PwnedPasswordsValidator",
            "OPTIONS": {
                "error_message": "Cannot use a compromised password. This password was detected %(amount)d time(s) on 'haveibeenpwned.com'.",
                "help_message": "Your password can't be a compromised password.",
            },
        },
    )


# Internationalization
LANGUAGE_CODE = "en-US"
TIME_ZONE = get_localzone_name()
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static Files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(DATA_DIR, "collectstatic")
STATIC_URL = BASE_URL + "/static/"
STATICFILES_DIRS = [
    USER_STATICFILES_DIR,
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "media/"
