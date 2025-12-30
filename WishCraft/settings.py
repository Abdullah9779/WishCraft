from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------------------
# BASE DIRECTORY
# -------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------
# BASIC SETTINGS
# -------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    'wishcraft.pythonanywhere.com',
    '127.0.0.1',
    'localhost',
]

ADMINS = [
    ('Site Admin', os.getenv('MAIL_SEND_TO')),
]


# -------------------------------------
# SECURITY SETTINGS — PYTHONANYWHERE SAFE
# -------------------------------------
CSRF_COOKIE_SECURE = True              # Only over HTTPS
SECURE_SSL_REDIRECT = True             # Force HTTPS
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 * 2         # 2 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
X_FRAME_OPTIONS = 'DENY'               # Prevent clickjacking
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True


# -------------------------------------
# SESSION SETTINGS
# -------------------------------------
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 * 2    # 2 year
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True      # Refresh expiry on each request
SESSION_COOKIE_SECURE = True           # Only over HTTPS
SESSION_COOKIE_HTTPONLY = True         # JS cannot access
SESSION_COOKIE_SAMESITE = 'Lax'        # Protect against CSRF


# -------------------------------------
# INSTALLED APPLICATIONS
# -------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "WishCraft_pages",
    "WishCraft_api",
    "WishCraft_admin_panel_protection",
]


# -------------------------------------
# MIDDLEWARE
# -------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "WishCraft_admin_panel_protection.middleware.AdminPanelProtectionMiddleware",
]


# -------------------------------------
# URLS AND TEMPLATES
# -------------------------------------
ROOT_URLCONF = "WishCraft.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "WishCraft.wsgi.application"


# -------------------------------------
# DATABASE
# -------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DATABASE_NAME'),
#         'USER': os.getenv('DATABASE_USER'),
#         'PASSWORD': os.getenv('DATABASE_PASSWORD'),
#         'HOST': os.getenv('DATABASE_HOST'),
#         'PORT': os.getenv('DATABASE_PORT'),
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'"
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------------------------------------
# PASSWORD VALIDATION
# -------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------
# INTERNATIONALIZATION
# -------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = '/static'

MEDIA_URL = "/media/"
MEDIA_ROOT = '/media'


# -------------------------------------
# EMAIL CONFIGURATION
# -------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
MAIL_SEND_TO = os.getenv('MAIL_SEND_TO')
SERVER_EMAIL = os.getenv('MAIL_SEND_TO')


# -------------------------------------
# CACHING
# -------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "django_cache",
    }
}


# -------------------------------------
# LOGGING
# -------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "wishcraft.log"),
        },
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
        "wishcraft": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
    },
}
