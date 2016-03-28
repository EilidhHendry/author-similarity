#!/bin/bash

trap "kill -TERM -$$" SIGINT
./scripts/celery_purge.sh
./venv/bin/python manage.py runserver &
./scripts/celery_beat.sh &
./scripts/celery_cam.sh &
./scripts/worker.sh &
./scripts/worker_filesystem.sh &
wait
