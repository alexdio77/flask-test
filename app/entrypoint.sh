#!/bin/bash

exec gunicorn main:app \
    --workers ${WORKERS:-5} \
    --bind ${BIND_HOST:-0.0.0.0}:${BIND_PORT:-8000} \
"$@"