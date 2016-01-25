import constants
import clean_up
import chunk
from compute_fingerprint import fingerprint_text

import celery
app = celery.Celery('tasks', backend="amqp", broker='amqp://guest@localhost//')

@app.task
def clean_text(input_path, author, title):
    return clean_up.clean_file(input_path, author, title)

@app.task
def chunk_text(input_path, author, title):
    return chunk.chunk_text(input_path, author, title)

@app.task
def compute_fingerprint(author_name, book_title, chunk_name, write_to_csv=True):
    return fingerprint_text(author_name, book_title, chunk_name, write_to_csv)
