#!/bin/sh

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --preload main:app --timeout 0 --workers $WORKERS 2>&1 | tee /var/log/messages-app.log

