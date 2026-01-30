from . import base  # noqa: F401
from decouple import config, Csv  # noqa: F401
for setting in dir(base):
    if setting.isupper():
        globals()[setting] = getattr(base, setting)


DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Всё, что специфично для разработки:
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
