from . import base  # noqa: F401
from decouple import config, Csv  # noqa: F401
for setting in dir(base):
    if setting.isupper():
        globals()[setting] = getattr(base, setting)

# Убираем дебаг и готовим себя к слезам:
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Настраивай это под боевой фронт
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv(), default='')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
