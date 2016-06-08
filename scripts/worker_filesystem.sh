#!/usr/bin/env bash
./venv/bin/celery worker --app=author_similarity --loglevel=info --queues=celery,filesystem --hostname=filesystem.%h
