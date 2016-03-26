#!/bin/bash

trap "kill -TERM -$$" SIGINT
./manage.py runserver &
./scripts/purge_celery.sh &
./scripts/beat.sh &
./scripts/cam.sh &
wait
