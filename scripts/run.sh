#!/bin/bash

trap "kill -TERM -$$" SIGINT
./manage.py runserver &
./scripts/celery.sh &
./scripts/beat.sh &
./scripts/cam.sh &
wait
