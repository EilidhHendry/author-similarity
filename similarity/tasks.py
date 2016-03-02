from celery import Celery, task, shared_task
from models import Text, Classifier, Chunk
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint
import classifier.svm

app = Celery('author_similarity')
from classifier import tasks

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
    print "Storing..."
    classifier.svm.store_classifier(clf)

    system_classifier.status = "trained"
    system_classifier.save()
    print "Trained the classifier"

@app.task
def process_text(text_id):
    print "Processing the text, id: %s" % (str(text_id))
    text = Text.objects.get(pk=text_id)

    print "Cleaning text..."
    classifier.clean_up.clean_file(text.text_file.path, text.author.name, text.name)
    cleaned_text_path = text.create_preprocessed_path()

    print "Chunking text..."
    chunk_number = 0
    for chunk_text in classifier.chunk.chunk_text(cleaned_text_path):
        print "Creating chunk: %s" % (str(chunk_number))
        chunk = Chunk.create(text, chunk_number, chunk_text)
        print "Saved chunk: %s" % (str(chunk_number))
        chunk_number+=1
    print "Processed the text"

@app.task
def process_chunk(chunk_id, chunk_text):
    print "Processing the chunk, id: %s" % (str(chunk_id))
    chunk = Chunk.objects.get(pk=chunk_id)

    # set fingerprint, skip author column
    print "Fingerprinting chunk..."
    fingerprint = classifier.compute_fingerprint.fingerprint_text(chunk_text)
    for key in fingerprint.keys():
        setattr(chunk, key, fingerprint[key])
    chunk.save()
