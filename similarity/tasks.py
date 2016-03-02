from celery import Celery, task, shared_task
from models import Classifier, Chunk
from classifier import svm

app = Celery('author_similarity')
from classifier import tasks

@app.task
def train_classifier(classifier_id):
    print "Training the classifier!!!"
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
    clf = svm.train_svm(fingerprints, authors)
    print "Storing..."
    svm.store_classifier(clf)

    system_classifier.status = "trained"
    system_classifier.save()
    print "Trained the classifier!!!"
