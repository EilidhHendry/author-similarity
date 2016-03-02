from celery import Celery, task, shared_task
from models import Text, Classifier, Chunk
import classifier.clean_up
import classifier.chunk
import classifier.compute_fingerprint

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
    clf = svm.train_svm(fingerprints, authors)
    print "Storing..."
    svm.store_classifier(clf)

    system_classifier.status = "trained"
    system_classifier.save()
    print "Trained the classifier"

@app.task
def process_text(text_id):
    print "Processing the text, id: %s" % (str(text_id))
    text = Text.objects.get(pk=text_id)
    print text

    print "Cleaning text..."
    classifier.clean_up.clean_file(text.text_file.path, text.author.name, text.name)
    cleaned_text_path = text.create_preprocessed_path()

    print "Chunking text..."
    text_chunks_path = classifier.chunk.generate_chunk_path(text.author.name, text.name)
    chunk_number = 0
    for chunk in classifier.chunk.chunk_text(cleaned_text_path):
        print "Fingerprinting chunk: %s" % (str(chunk_number))
        fingerprint = classifier.compute_fingerprint.fingerprint_text(chunk)
        theChunk = Chunk.create(text, chunk_number, fingerprint)
        print "Saving chunk..."
        theChunk.save()
        chunk_number+=1
    print "Processed the text"
