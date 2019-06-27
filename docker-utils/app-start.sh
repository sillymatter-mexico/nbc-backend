#!/bin/bash

echo "Starting uWSGI for ${PROJECT_NAME}"



uwsgi --chdir ${SITE_DIR}proj/ \
    --module=${PROJECT_NAME}.wsgi:application \
    --master \
    --vacuum \
    --max-requests=5000 \
    --socket 0.0.0.0:8000 \
    --processes $NUM_PROCS \
    --threads $NUM_THREADS \
    --python-autoreload=1

#    --static-map /static=${SITE_DIR}htdocs/static/ \
#    --static-map /media=${SITE_DIR}htdocs/media/ \

exit