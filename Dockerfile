# Debian based image
FROM python:3.6

# reduce image size by cleaning up after install
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    libfreetype6 \
    libfreetype6-dev \
    libpq-dev \
    postgresql-client \
    zlib1g-dev \
    ruby-sass \
    python-m2crypto \
    swig \
    binutils \
    libproj-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# set the environment variable default; can be overridden by compose
ENV SITE_DIR=/site/
RUN mkdir -p $SITE_DIR
WORKDIR $SITE_DIR
RUN mkdir -p proj/ var/log/ htdocs/
# create a virtualenv to separate app packages from system packages
#COPY docker-utils/ssl/ ssl/

# pre-install requirements; doing this sooner prevents unnecessary layer-building
COPY requirements.txt requirements.txt
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
# Make sure that we install uwsgi, regardless of project requirements
RUN pip install uwsgi
# Set some environment variables; can be overridden by compose
ENV NUM_THREADS=8
ENV NUM_PROCS=2

# Copy in docker scripts
COPY docker-utils/ docker-utils/


ENV SECRET_KEY='65yys=&@7ox9*m46%w@t%@c3o=#19%ju)5otg85)n#+9jg&cr!'
ENV DJANGO_SETTINGS_MODULE='universal.settings.develop'
ENV BROKER_URL='amqp://guest:guest@rabbitmq:5672/'
ENV DB_NAME='universal'
ENV DB_USER='postgres'
ENV DB_PASSWORD=''
ENV DB_HOST='db'
ENV DB_PORT='5432'
ENV EMAIL_USE_TLS = 'True'
ENV EMAIL_HOST = 'smtp.gmail.com'
ENV EMAIL_HOST_USER = 'claudiam.texcucano@gmail.com'
ENV EMAIL_HOST_PASSWORD = 'claudia333ale'
ENV EMAIL_PORT = '587'
ENV EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

COPY . proj/
