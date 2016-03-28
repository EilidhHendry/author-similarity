./venv/bin/celery worker --app=author_similarity --loglevel=info --queues=filesystem --hostname=filesystem.%h
