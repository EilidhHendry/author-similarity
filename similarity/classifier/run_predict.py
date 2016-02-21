#!/usr/bin/python

import constants
from compute_fingerprint import fingerprint_text
from svm import load_classifier
import time

if __name__ == "__main__":
    print time.ctime()
    print "fingerprinting"
    fingerprint_list = fingerprint_text('hemingway', 'completeshortstories', '0000.txt')

    print "loading classifier"
    clf = load_classifier(constants.MODEL_PATH)

    print "predicting"
    prediction = clf.predict(fingerprint_list[1:])

    print prediction
    print time.ctime()

__author__ = 'eilidhhendry'
