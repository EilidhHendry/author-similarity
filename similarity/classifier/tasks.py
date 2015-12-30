import constants
import chunk
import clean_up
from compute_fingerprint import compute_fingerprint

import celery
app = celery.Celery('tasks', backend="amqp", broker='amqp://guest@localhost//')

@app.task
def clean_text(input_path, author, title):
    return clean_up.clean_file(input_path, author, title)

@app.task
def chunk_text(input_path, author, title, chunk_size=constants.CHUNK_SIZE):
    return chunk.chunk_text(input_path, author, title, chunk_size)

@app.task
def compute_fingerprint(author_name, book_title, chunk_name, write_to_csv=True):
    return compute_fingerprint(author_name, book_title, chunk_name, write_to_csv)
