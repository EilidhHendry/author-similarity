#!/usr/bin/env python
from clean_up import clean_directories
from chunk import chunk_dir
from compute_fingerprint import compute_all_fingerprints
from combine_chunks import combine_chunks
from svm import train_svm, svm_accuracy, store_classifier, load_classifier

if __name__ == "__main__":
    print "cleaning text"
    clean_directories()
    print "chunking"
    chunk_dir()
    print "fingerprinting"
    compute_all_fingerprints()
    print "combining"
    combine_chunks()

    print "training"
    clf, test_data, test_targets = train_svm()
    print "storing"
    store_classifier(clf)

    print "loading"
    clf = load_classifier()
    print "testing"
    accuracy = svm_accuracy(clf, test_data, test_targets)
    print "accuracy:" + str(accuracy)
