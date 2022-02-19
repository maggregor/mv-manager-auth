"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import datetime
import io
import os
import environ

from pathlib import Path
from django.core.management.utils import get_random_secret_key
import google.auth
from google.cloud import secretmanager


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# [START cloudrun_django_secret_config]
# SECURITY WARNING: don't run with debug turned on in production!
# Change this to "False" when you are ready for production
env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END cloudrun_django_secret_config]


SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")



# env = environ.Env(DEBUG=(int, 0))
# # reading .env file
# environ.Env.read_env(".env")



# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env.str("DJANGO_SECRET_KEY", default=get_random_secret_key())

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool("DEBUG", default=True)

BASE_BACKEND_URL = env.str("DJANGO_BASE_BACKEND_URL", default="http://localhost:8000")
BASE_FRONTEND_URL = env.str("DJANGO_BASE_FRONTEND_URL", default="http://localhost:8081")

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        ".herokuapp.com",
        "auth.achilio.com",
        "beta.auth.achilio.com",
        "dev.auth.achilio.com"
    ],
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_jwt",
    "rest_framework_jwt.blacklist",
    "rest_framework_api_key",
    "users",
    "storages"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# [END cloudrun_django_database_config]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# [START cloudrun_django_static_config]
# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATIC_URL = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"
# [END cloudrun_django_static_config]

# Custom user model
AUTH_USER_MODEL = "users.User"

PRODUCTION_SETTINGS = env.bool("DJANGO_PRODUCTION_SETTINGS", default=False)

# JWT settings
JWT_EXPIRATION_DELTA_DEFAULT = 2.628e6  # 1 month in seconds
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(
        seconds=env.int(
            "DJANGO_JWT_EXPIRATION_DELTA", default=JWT_EXPIRATION_DELTA_DEFAULT
        )
    ),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_GET_USER_SECRET_KEY": lambda user: user.secret_key,
    "JWT_RESPONSE_PAYLOAD_HANDLER": "users.selectors.jwt_response_payload_handler",
    "JWT_AUTH_COOKIE": "jwt_token",
    "JWT_AUTH_COOKIE_SAMESITE": "None",
}


# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list(
    "DJANGO_CORS_ORIGIN_WHITELIST", default=[BASE_FRONTEND_URL]
)

# Google OAuth2 settings
GOOGLE_OAUTH2_CLIENT_ID = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_ID", "")
GOOGLE_OAUTH2_CLIENT_SECRET = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET", "")
