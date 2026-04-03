from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY", default=config("SECRET_KEY", default='django-insecure-gv5(6@9=ebjr7&$gi!e*ivg)#id56495w14*#=az%^nvz2__ks'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

# Hosts e origins obrigatórios — sempre presentes independente de env vars
_ALLOWED_HOSTS_BASE = [
    "localhost",
    "127.0.0.1",
    ".railway.app",
]

_CSRF_ORIGINS_BASE = [
    "http://localhost",
    "http://127.0.0.1",
]

# Permite extensão via env var (ex.: novo domínio no futuro)
_extra_hosts = [h.strip() for h in config("DJANGO_ALLOWED_HOSTS", default="", cast=Csv()) if h.strip()]
_extra_origins = [o.strip(' "\'') for o in config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv()) if o.strip(' "\'')]

# Tratamento para Scheme HTTPS obrigatório no CSRF do Django 4+
_safe_origins = []
for orig in _extra_origins:
    if orig and not orig.startswith('http'):
        _safe_origins.append('https://' + orig)
    else:
        _safe_origins.append(orig)

ALLOWED_HOSTS = ["*"]  # Permite qualquer host para evitar erros 400 (seguro no Railway)
CSRF_TRUSTED_ORIGINS = list({*_CSRF_ORIGINS_BASE, *_safe_origins})


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps do projeto
    "app_elleva",
    "pwa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pro_elleva.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pro_elleva.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    ENGINE_MAP = {
        "mysql": "django.db.backends.mysql",
        "mysql2": "django.db.backends.mysql",
        "postgres": "django.db.backends.postgresql",
        "postgresql": "django.db.backends.postgresql",
    }
    engine = ENGINE_MAP.get(url.scheme)
    if engine:
        DATABASES = {
            "default": {
                "ENGINE": engine,
                "NAME": url.path.lstrip("/"),
                "USER": url.username or "",
                "PASSWORD": url.password or "",
                "HOST": url.hostname or "",
                "PORT": str(url.port or "3306"),
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }


# Password validation
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


# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================================================================
# SEGURANÇA - RAILWAY E PROXIES
# ===================================================================
# Necessário no Railway para Django reconhecer requests HTTPS atrás de proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Ativa segurança HTTPS e Cookies Seguros se estivermos em Produção (DEBUG=False)
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# ===================================================================
# PWA CONFIGURATION
# ===================================================================
PWA_APP_NAME = "Elleva Odontologia"
PWA_APP_DESCRIPTION = "Clínica Odontológica Especializada"
PWA_APP_THEME_COLOR = "#e73111"
PWA_APP_BACKGROUND_COLOR = "#FDFBFA"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {
        "src": "/static/logo_elleva.jpg",
        "sizes": "192x192"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "/static/logo_elleva.jpg",
        "sizes": "192x192"
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "pt-BR"
