#!/bin/bash

echo "Starting Celerybeat for ${PROJECT_NAME}"

if [ -e "/site/celerybeat.pid" ]
then
    rm "/site/celerybeat.pid"
    echo "delete celerybeat.pid"
else
    echo "sin archivo"
fi
celery -A ${PROJECT_NAME} worker --beat --workdir /site/proj/ -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

exit