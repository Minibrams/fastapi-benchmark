#!/bin/bash

N_WORKERS=1
BIND=0.0.0.0:4242
WORKER_CLASS=uvicorn.workers.UvicornWorker

exec gunicorn 'api:app' \
    --bind=$BIND \
    --workers=$N_WORKERS \
    --worker-class=$WORKER_CLASS
