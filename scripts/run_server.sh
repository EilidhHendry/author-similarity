#!/bin/bash

trap "kill -TERM -$$" SIGINT
./scripts/celery_purge.sh
./scripts/celery_beat.sh &
./scripts/celery_cam.sh &
./scripts/worker.sh &
./scripts/worker_filesystem.sh &
wait
