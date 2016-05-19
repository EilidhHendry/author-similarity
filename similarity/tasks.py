from celery import Celery, task, shared_task

from models import Text, Classifier, Chunk, Author
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint
import classifier.svm

@shared_task
def periodic_retrain():
    print "Periodic classifier training"
    system_classifier = Classifier.objects.first()
    print "Classifier status: %s" % (system_classifier.status)
    if (system_classifier.status == "untrained"):
        train_classifier.delay()
        return True
    else:
        return False

@shared_task
def train_classifier():
    print "Training the classifier"
    system_classifier = Classifier.objects.first()
    system_classifier.status = "training"
    system_classifier.save()

    print "Fetching Chunks"
    chunks = Chunk.get_chunks()
    authors = []
    fingerprints = []
    for chunk in chunks:
        if chunk.author:
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

@shared_task(queue="filesystem")
def store_trained_classifier(clf):
    if (clf is None):
        print "No classifier to store"
        return None
    print "Storing classifier"
    system_classifier = Classifier.objects.first()
    classifier.svm.store_classifier(clf)
    system_classifier.status = "trained"
    system_classifier.save()
    print "Stored classifier"
    return True

@shared_task
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

@shared_task
def create_average_chunk(instance_id, instance_type):
    instance = instance_type.objects.get(pk=instance_id)
    if (instance.average_chunk is not None):
        instance.average_chunk.delete()

    chunks = []
    if isinstance(instance, Text):
        chunks = Chunk.get_chunks().filter(text=instance)
    elif isinstance(instance, Author):
        chunks = Chunk.get_chunks().filter(author=instance)

    print "averaging %i chunks" % (len(chunks))
    average_fingerprint = Chunk.get_average_fingerprint_of_chunks(chunks)
    chunk = Chunk.objects.create()
    for key in average_fingerprint.keys():
        setattr(chunk, key, average_fingerprint[key])

    if isinstance(instance, Text):
        chunk.text = instance
    elif isinstance(instance, Author):
        chunk.author = instance
    chunk.save()
    instance.average_chunk = chunk
    instance.save()
