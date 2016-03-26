#!/bin/bash

trap "kill -TERM -$$" SIGINT
./scripts/purge_celery.sh &
./scripts/beat.sh &
./scripts/cam.sh &
wait
