from .base import *
from unipath import Path

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': 5432,
    }
}
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = os.getenv('BROKER_URL')
CELERY_DISABLE_RATE_LIMITS = True


STATIC_ROOT = Path(os.path.abspath(__file__)).ancestor(4).child('htdocs',
                                                                'static')
