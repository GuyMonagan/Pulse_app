from .base import *

# Убираем дебаг и готовим себя к слезам:
DEBUG = False

# Настраивай это под боевой фронт
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://your-frontend-domain.com',
]

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
