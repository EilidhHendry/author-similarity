# -*- coding: utf-8 -*-,

__author__ = 'eilidhhendry'

import nltk
import ast
from collections import defaultdict


def get_freqdist():

    tagged_corpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader('training_data/split_10000_data_tagged/', r'.*\.txt$', cat_pattern=r'(\w+)/*')
    untagged_corpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader('split_10000_data/', r'.*\.txt$', cat_pattern=r'(\w+)/*')
    taglist = 'PRP PRP$ WP WP$ CC MD UH RP IN TO WDT DT PDT'.split()
    output_file = open('function_word_counts/1000_split_function_counts.txt', 'w')

    # loop through all the categories (authors)
    for category in tagged_corpus.categories():

        # loop through all the files (texts) in the current category (authors)
        for filename in tagged_corpus.fileids(category):

            pos_corpus = tagged_corpus.raw(fileids=filename)
            tuple_corpus = ast.literal_eval(pos_corpus)
            word_fd = nltk.FreqDist(word.lower() for (word, tag) in tuple_corpus if tag in taglist)
            word_count = len(untagged_corpus.words(fileids=filename))
            for word, count in word_fd.items():
                word_fd[word] = float(count)/word_count
            print>>output_file, filename, '\t', word_fd.items()



