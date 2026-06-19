"""
Settings — Tropicana Pio Pio Backend
Sécurisé : SECRET_KEY + DB + Email via variables d'environnement.
"""
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Charger les variables depuis backend/.env (dev) ou depuis l'environnement système (prod)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Sécurité ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-insecure-key-change-before-deploy')

# ⚠️ IMPORTANT : mettre DEBUG=False dans le .env de production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')

# Sécurité : empêcher le déploiement accidentel en mode debug avec un vrai domaine
_real_hosts = [h for h in ALLOWED_HOSTS if h not in ('localhost', '127.0.0.1', '')]
if DEBUG and _real_hosts:
    import warnings
    warnings.warn(
        f"⚠️  DEBUG=True avec des domaines de production ({_real_hosts}). "
        "Définissez DEBUG=False dans votre .env avant de déployer.",
        stacklevel=2
    )

# ── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',   # ✅ CORRECTION 7 : blacklist activée
    'corsheaders',
    # Local
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'tropicana_backend.urls.admin_guard',              # ✅ Protège /admin/ par IP en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tropicana_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'api' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tropicana_backend.wsgi.application'

# ── Base de données ───────────────────────────────────────────────────────────
# ✅ CORRECTION 3 : PostgreSQL en production, SQLite en développement
if os.environ.get('DATABASE_URL'):
    import dj_database_url  # pip install dj-database-url
    DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
elif os.environ.get('DB_NAME'):
    # PostgreSQL configuré manuellement
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':     os.environ.get('DB_NAME', 'tropicana_db'),
            'USER':     os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST':     os.environ.get('DB_HOST', 'localhost'),
            'PORT':     os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # SQLite — développement local uniquement
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Auth ─────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'api.Utilisateur'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# ── Fichiers statiques & médias ───────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ CORRECTION — Taille max upload (vidéos témoignages : 100 Mo)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10_485_760    # 10 Mo
FILE_UPLOAD_MAX_MEMORY_SIZE = 10_485_760

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Django REST Framework ─────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # ✅ Pagination globale
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # ✅ Protection brute-force renforcée
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
        'user': '100/minute',
        'auth': '5/minute',
        'contact': '3/minute',
        'webhook': '200/minute',
    },
}

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} — {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'api.securite': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ── JWT ───────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),   # ✅ Réduit de 60 à 30 min
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),        # ✅ Réduit de 30 à 7 jours
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'UPDATE_LAST_LOGIN': True,                          # ✅ Trace la dernière connexion
}

# ── CORS ──────────────────────────────────────────────────────────────────────
_cors_raw = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_raw.split(',') if o.strip()]
CORS_ALLOW_ALL_ORIGINS = False  # ✅ Toujours explicitement désactivé
CORS_ALLOW_CREDENTIALS = True
# ── Email timeout ──────────────────────────────────────────────────────────────
EMAIL_TIMEOUT = 5  # secondes

# ── Email ─────────────────────────────────────────────────────────────────────
# ✅ CORRECTION 4 : SMTP réel via variables d'environnement
if os.environ.get('EMAIL_HOST_USER'):
    EMAIL_BACKEND    = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST       = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT       = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS    = True
    EMAIL_HOST_USER  = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
else:
    # Développement : emails affichés dans la console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'Tropicana Pio Pio <tropicanapiopio.officiel@gmail.com>'

# ── Google OAuth ──────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')

# ── Sécurité HTTPS (production uniquement) ───────────────────────────────────
if not DEBUG:
    SECURE_HSTS_SECONDS            = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_BROWSER_XSS_FILTER      = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Frontend URL (pour les liens dans les emails) ─────────────────────────────
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

# ── Admin IP whitelist (optionnel — laisser vide = accès ouvert à tous les admins) ──
# En production, définir ADMIN_ALLOWED_IPS=1.2.3.4,5.6.7.8 dans .env
_admin_ips_raw = os.environ.get('ADMIN_ALLOWED_IPS', '')
ADMIN_ALLOWED_IPS = [ip.strip() for ip in _admin_ips_raw.split(',') if ip.strip()]


# ── Fedapay ───────────────────────────────────────────────────────────────────
FEDAPAY_PUBLIC_KEY     = os.environ.get('FEDAPAY_PUBLIC_KEY', '')
FEDAPAY_SECRET_KEY     = os.environ.get('FEDAPAY_SECRET_KEY', '')
FEDAPAY_ENV            = os.environ.get('FEDAPAY_ENV', 'sandbox')
FEDAPAY_WEBHOOK_SECRET = os.environ.get('FEDAPAY_WEBHOOK_SECRET', '')
FRONTEND_URL           = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
