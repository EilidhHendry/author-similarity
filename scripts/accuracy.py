from similarity.models import *
from similarity.classifier import svm
chunks = Chunk.objects.all()
authors = []
fingerprints = []
for chunk in chunks:
	authors.append(chunk.author.name)
	fingerprints.append(chunk.get_fingerprint_list())
mean = svm.find_classifier_accuracy(fingerprints, authors)
print "Accuracy: ", mean
