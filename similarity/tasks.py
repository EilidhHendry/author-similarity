from celery import Celery, task, shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from models import Text, Classifier, Chunk, Author
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint
import classifier.svm

app = Celery('author_similarity')

@app.task
def periodic_retrain():
    print "Periodic classifier training"
    system_classifier = Classifier.objects.first()
    print "Classifier status: %s" % (system_classifier.status)
    if (system_classifier.status == "untrained"):
        train_classifier.delay()
        return True
    else:
        return False

@app.task
def train_classifier():
    print "Training the classifier"
    system_classifier = Classifier.objects.first()
    system_classifier.status = "training"
    system_classifier.save()

    print "Fetching Chunks"
    chunks = Chunk.objects.all()
    authors = []
    fingerprints = []
    for chunk in chunks:
        authors.append(chunk.author.name)
        fingerprints.append(chunk.get_fingerprint_list())

    print "Training..."
    clf = classifier.svm.train_svm(fingerprints, authors)
    if clf:
        print "Trained the classifier"
        store_trained_classifier.delay(clf)
        return True
    else:
        print "Failed to train classifier"
        system_classifier.status = "untrained"
        system_classifier.save()
        return False

@app.task
def store_trained_classifier(clf):
    print "Storing classifier"
    system_classifier = Classifier.objects.first()
    classifier.svm.store_classifier(clf)
    system_classifier.status = "trained"
    system_classifier.save()
    print "Stored classifier"
    return True

@app.task
def add_chunk(author_id, text_id, text_chunk_number, chunk_text):
    print "Creating chunk: %s" % (str(text_chunk_number))
    chunk = Chunk(author_id=author_id, text_id=text_id, text_chunk_number=text_chunk_number)
    print "Fingerprinting chunk"
    fingerprint = classifier.compute_fingerprint.fingerprint_text(chunk_text)
    for key in fingerprint.keys():
        setattr(chunk, key, fingerprint[key])
    chunk.save()
    print "Processed chunk with id %s" % (str(chunk.id))
    return True
