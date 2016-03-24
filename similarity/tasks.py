from celery import Celery, task, shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from models import Text, Classifier, Chunk
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint
import classifier.svm

app = Celery('author_similarity')

@app.task
def periodic_retrain():
    print "Periodic classifier training"
    system_classifier = Classifier.objects.first()
    system_classifier_id = system_classifier.id
    print "Classifier status: %s" % (system_classifier.status)
    if (system_classifier.status == "untrained"):
        train_classifier(system_classifier_id)

@app.task
def train_classifier(classifier_id):
    print "Training the classifier, id: %s" % (str(classifier_id))
    system_classifier = Classifier.objects.get(pk=classifier_id)
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
        print "Storing..."
        classifier.svm.store_classifier(clf)
        system_classifier.status = "trained"
        system_classifier.save()
        print "Trained the classifier"
        return True
    else:
        system_classifier.status = "untrained"
        system_classifier.save()
        print "Failed to train classifier"
        return False

@app.task
def process_chunk(chunk_id, chunk_text):
    print "Processing the chunk with id: %s" % (str(chunk_id))
    try:
        chunk = Chunk.objects.get(pk=chunk_id)
        print "Fingerprinting chunk"
        fingerprint = classifier.compute_fingerprint.fingerprint_text(chunk_text)
        for key in fingerprint.keys():
            setattr(chunk, key, fingerprint[key])
        chunk.save()
        print "processed chunk: %s" % (str(chunk_id))
        return True
    except Chunk.DoesNotExist:
        print "FAILED TO FIND THE CHUNK!"
        return False
