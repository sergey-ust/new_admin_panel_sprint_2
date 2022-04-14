#!/usr/bin/env bash

PROCESSOR_COUNT=$(nproc)
GUNICORN_WORKER_COUNT=$(( PROCESSOR_COUNT * 2 + 1 ))

gunicorn -w ${GUNICORN_WORKER_COUNT} -b 0.0.0.0:9808 app:application