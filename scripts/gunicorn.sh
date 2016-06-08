#!/usr/bin/env bash
./venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8003 author_similarity.wsgi:application
