from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = Path(__file__).resolve().parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--m$x*8jdxs27&xjxekj62d5x*o+2oz_d@4ekix7gv-@d-u3gpd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'talabalar-boshqaruv-sistemasi.herokuapp.com',
    'tbs-production.up.railway.app',
    'ozsmanagement.com',
    'www.ozsmanagement.com',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'fontawesomefree',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # "debug_toolbar",
    'TBS_app',
    'phone_field', 
    # 'storages'
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'TBS_app.LoginCheckMiddleWare.LoginCheckMiddleWare',
    'whitenoise.middleware.WhiteNoiseMiddleware',


]

ROOT_URLCONF = 'TBS_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # "/home/html/tbs-production.up.railway.app.com",
            # "/home/html/default",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'TBS_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'rSe967UjBt9phR0GbqRw',
        'HOST': 'containers-us-west-41.railway.app',
        'PORT': '7112',  # django uses usefully 5432 port that is the postegres port

    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# For Custom USER
AUTH_USER_MODEL = "TBS_app.CustomUser"

# Registering Custom Backend "EmailBackEnd"
AUTHENTICATION_BACKENDS = ['TBS_app.EmailBackEnd.EmailBackEnd']

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    'https://ozsmanagement.com',
    'https://www.ozsmanagement.com',
    'http://ozsmanagement.com',
    'http://www.ozsmanagement.com',
    'http://tbs-production.up.railway.app'

]

CORS_REPLACE_HTTPS_REFERER = True

CSRF_COOKIE_DOMAIN = 'tbs-production.up.railway.app'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

CORS_ORIGIN_WHITELIST = (
    'https://ozsmanagement.com',
    'http://ozsmanagement.com',
    'ozsmanagement.com',
    'https://tbs-production.up.railway.app',
    'http://tbs-production.up.railway.app',
    'tbs-production.up.railway.app',
    'talabalar-boshqaruv-sistemasi.herokuapp.com'
    'https://talabalar-boshqaruv-sistemasi.herokuapp.com'
    'http://talabalar-boshqaruv-sistemasi.herokuapp.com'
)


# # S3 
# AWS_ACCESS_KEY_ID = 'AKIA5ETDILD6GADA524M'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'ozsmanagement'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-north-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# STATICFILES_LOCATION = 'static'
# MEDIAFILES_LOCATION = 'media'

# AWS_ACCESS_KEY_ID = 'AKIA5ETDILD6GADA524M'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'ozsmanagement'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_HOST = 's3.eu-north-1.amazonaws.com'
# AWS_S3_REGION_NAME = 'eu-north-1'

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.eu-north-1.amazonaws.com'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# MEDIA_ROOT = os.path.join (BASE_DIR, 'media')
# STATIC_ROOT = os.path.join (BASE_DIR, 'static')

# STATIC_URL = AWS_S3_CUSTOM_DOMAIN + '/static/' 
# MEDIA_URL = AWS_S3_CUSTOM_DOMAIN + '/media/' 