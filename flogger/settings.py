import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ... existing settings ...
STATIC_URL = 'static/'
# This is the line you are missing:
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

# Optional: If you have a global static folder for your project
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "127.0.0.1",
    "flogger-4kpc.onrender.com",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "markdownify.apps.MarkdownifyConfig",
    "user_profile",
    "blog",
    "django_htmx",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'user_profile.middleware.JWTAuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]


if DEBUG:
    print('===== -----* DEBUG ENVIRONMENT *----- =====')
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(
        1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

INTERNAL_IPS = [
    "127.0.0.1",
]

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")

if ENVIRONMENT == "PROD":
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.2,
        send_default_pii=False,
        environment=ENVIRONMENT,
    )

ROOT_URLCONF = 'flogger.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'flogger.wsgi.application'

# Replace the DATABASES section of your settings.py with this
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production (Neon / hosted postgres)
    config = urlparse(DATABASE_URL)

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.path.lstrip("/"),
            "USER": config.username,
            "PASSWORD": config.password,
            "HOST": config.hostname,
            "PORT": config.port or 5432,
            "OPTIONS": {
                "sslmode": os.getenv("NEON_SSL","disable"),   # required for Neon
            },
        }
    }

else:
    # Local postgres
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "flog_db"),
            "USER": os.getenv("DB_USER", "flog_user"),
            "PASSWORD": os.getenv("DB_PASS", "django_pass"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

AUTH_USER_MODEL = 'user_profile.User'

CSRF_COOKIE_PATH = "/"
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code', 
            'span', 'strong', 'em', 'br', 'ul', 'li', 'ol'
        ],
        "MARKDOWN_EXTENSIONS": [
            "markdown.extensions.fenced_code",
            "markdown.extensions.extra",
            "markdown.extensions.nl2br",
        ],
    }
}

# JWT settings
JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TTL = 15 * 60 * 60    # 15 minutes
JWT_REFRESH_TTL = 7 * 24 * 3600  # 7 days
