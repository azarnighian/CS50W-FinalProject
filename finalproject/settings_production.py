# https://devcenter.heroku.com/articles/django-app-configuration
# https://devcenter.heroku.com/articles/deploying-python 
import django_heroku


DEBUG = False

# https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

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

ALLOWED_HOSTS = ['trovare1.herokuapp.com']

# https://docs.djangoproject.com/en/3.2/topics/logging/
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

MIDDLEWARE = [        
    'django.middleware.security.SecurityMiddleware',    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# https://help.heroku.com/J2R1S4T8/can-heroku-force-an-application-to-use-ssl-tls
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())