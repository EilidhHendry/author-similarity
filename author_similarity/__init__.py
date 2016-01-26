from __future__ import absolute_import

# ensure app is imported when Django starts
# (shared_task will use this app)
from .celery import app as celery_app
