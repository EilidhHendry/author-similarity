#!/usr/bin/env python
import time

from clean_up import clean_directories
from chunk import chunk_dir
from compute_fingerprint import compute_all_fingerprints
from combine_chunks import combine_chunks
from svm import find_classifier_accuracy
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
    fingerprints = compute_all_fingerprints()
    print (time.time() - last_time)
    last_time = time.time()

    #TODO: cannot find svm accuracy without being able to obtain list of targets
