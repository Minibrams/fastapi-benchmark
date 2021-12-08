#!/bin/bash

N_WORKERS=1
BIND=127.0.0.1:4242
WORKER_CLASS=uvicorn.workers.UvicornWorker
FLASK_WORKER=sync

#exec gunicorn --bind=$BIND --workers=$N_WORKERS --worker-class=$FLASK_WORKER --reload 'api:app'

exec gunicorn 'api:app' \
    --bind=$BIND \
    --workers=$N_WORKERS \
    --worker-class=$WORKER_CLASS \
    --reload
