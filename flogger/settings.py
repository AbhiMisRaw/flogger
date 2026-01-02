import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse, parse_qsl
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
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
    # "rest_framework_simplejwt",
    "markdownify.apps.MarkdownifyConfig",
    "user_profile",
    "blog",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases


# Replace the DATABASES section of your settings.py with this
POSTGERS_CONFIG = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGERS_CONFIG.path.lstrip('/'),
        'USER': POSTGERS_CONFIG.username,
        'PASSWORD': POSTGERS_CONFIG.password,
        'HOST': POSTGERS_CONFIG.hostname,
        'PORT': POSTGERS_CONFIG.port or 5432,
        # neon DB
        # 'NAME': POSTGERS_CONFIG.path.replace('/', ''),
        # 'USER': POSTGERS_CONFIG.username,
        # 'PASSWORD': POSTGERS_CONFIG.password,
        # 'HOST': POSTGERS_CONFIG.hostname,
        # 'PORT': 5432,
        # 'OPTIONS': dict(parse_qsl(POSTGERS_CONFIG.query)),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

# JWT Setting
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': True,

#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,

#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',

# }


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'


# listings/settings.py
...
AUTH_USER_MODEL = 'user_profile.User'

CSRF_COOKIE_PATH = "/"   # ✅ safest
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
            "markdown.extensions.fenced_code",  # This handles the ``` blocks
            "markdown.extensions.extra",        # Adds support for tables, etc.
            "markdown.extensions.nl2br",        # Preserves your newlines
        ],
    }
}