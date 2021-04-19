"""
Django settings for finalproject project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os

import environ

# https://devcenter.heroku.com/articles/django-app-configuration
# https://devcenter.heroku.com/articles/deploying-python 
import django_heroku


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# For environment variable (for secret key)
    # https://djangocentral.com/environment-variables-in-django/
env = environ.Env()
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
# with open('/Users/azarnighian/Desktop/CS50W/Final Project/finalproject/finalproject/secret_key.txt') as f:
#     SECRET_KEY = f.read().strip()
# PRODUCTION:
# https://stackoverflow.com/questions/47949022/git-heroku-how-to-hide-my-secret-key
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment#getting_your_website_ready_to_publish
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
SECRET_KEY = env("DJANGO_SECRET_KEY")


# PRODUCTION:
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# PRODUCTION:
# https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# PRODUCTION:
# For getting error emails
    # https://docs.djangoproject.com/en/3.1/howto/error-reporting/#server-errors
    # https://stackoverflow.com/questions/6367014/how-to-send-email-via-django
ADMINS = [('Aharon', env("GMAIL_USERNAME"))]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env("GMAIL_USERNAME")
EMAIL_HOST_PASSWORD = env("GMAIL_APP_PASSWORD")
EMAIL_PORT = 587


# PRODUCTION:
# ALLOWED_HOSTS = ['trovare1.herokuapp.com', '127.0.0.1']
ALLOWED_HOSTS = ['*']

# PRODUCTION:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}


# Application definition

INSTALLED_APPS = [
    'restaurants',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
        # PRODUCTION^
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finalproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'finalproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = "restaurants.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'staticfiles'
    # PRODUCTION^

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# PRODUCTION:
# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# PRODUCTION:
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# PRODUCTION:
# Activate Django-Heroku.
django_heroku.settings(locals())