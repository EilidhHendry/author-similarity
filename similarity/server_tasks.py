from celery import Celery, task
from models import Classifier
import classifier.svm

app = Celery('author_similarity')
@app.task
def store_trained_classifier(clf):
    print "Storing classifier"
    system_classifier = Classifier.objects.first()
    classifier.svm.store_classifier(clf)
    system_classifier.status = "trained"
    system_classifier.save()
    print "Stored classifier"
