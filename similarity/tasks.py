from celery import Celery, task, shared_task

app = Celery('author_similarity')
from classifier import tasks
