#!/usr/bin/env python
import time

from clean_up import clean_directories
from chunk import chunk_dir
from compute_fingerprint import compute_all_fingerprints
from combine_chunks import combine_chunks
from svm import read_csv, find_classifier_accuracy
import constants

if __name__ == "__main__":
    last_time = time.time()
    print "cleaning text"
    clean_directories()
    print (time.time() - last_time)

    last_time = time.time()
    print "chunking"
    chunk_dir()
    print (time.time() - last_time)
    last_time = time.time()

    print "fingerprinting"
    compute_all_fingerprints()
    print (time.time() - last_time)
    last_time = time.time()

    print "combining"
    combine_chunks()
    print (time.time() - last_time)
    last_time = time.time()

    print "training"
    training_data = []
    targets = []
    # reads from csv and overwrites given values for training_data and targets
    if constants.CSV:
        training_data, targets = read_csv(constants.COMBINED_FINGERPRINT_FILE_PATH)
    accuracy = find_classifier_accuracy(training_data, targets)
    print (time.time() - last_time)
    last_time = time.time()

    print "accuracy:" + str(accuracy)
