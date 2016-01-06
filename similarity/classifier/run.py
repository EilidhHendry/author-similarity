#!/usr/bin/python
import constants
from clean_up import clean_directories
from chunk import chunk_dir
from compute_fingerprint import compute_all_fingerprints
from combine_chunks import combine_chunks
from svm import train_csv, svm_accuracy, store_classifier, load_classifier

if __name__ == "__main__":
    print "cleaning text"
    clean_directories(constants.PLAINTEXT_PATH)

    print "chunking"
    chunk_dir(constants.PREPROCESSED_PATH, constants.CHUNK_SIZE)

    print "fingerprinting"
    compute_all_fingerprints(constants.CHUNKS_PATH)

    print "training"
    combine_chunks(constants.FINGERPRINTS_PATH)
    clf, test_data, test_targets = train_csv(constants.COMBINED_FINGERPRINT_FILE_PATH)

    print "storing"
    store_classifier(clf, constants.MODEL_PATH)
    print "loading"
    clf = load_classifier(constants.MODEL_PATH)

    print "testing"
    accuracy = svm_accuracy(clf, test_data, test_targets)

    print "accuracy:"
    print accuracy
