# -*- coding: utf-8 -*-,

__author__ = 'eilidhhendry'

import nltk
import ast
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def get_freqdist():

    tagged_corpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader('split_10000_data_tagged/', r'.*\.txt$', cat_pattern=r'(\w+)/*')
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


def most_common():
    output_file = open('function_words.txt', 'w')
    function_words=defaultdict(int)
    with open('function_counts.txt') as infile:
        for line in infile:
            tuple_line = ast.literal_eval(line)
            for word, count in tuple_line:
                function_words[word]+=count

    sorted_function_words = sorted(function_words.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_function_words:
        print>>output_file, word, count


def plot_common():
    words_list = []
    word_count = []
    with open('function_words.txt') as infile:
        for line in infile:
            word, count = line.strip().split()
            words_list.append(word)
            word_count.append(int(count))
    print words_list[:51]
    print len(words_list[:51])
    print word_count
    plt.bar(range(len(word_count)), word_count)
    plt.xticks(range(len(words_list)), words_list, size='small', rotation='vertical')
    plt.xlim(0,len(words_list))
    plt.show()

def plot(hemingway, steinbeck, nabokov, wallace):

    fig = plt.figure()
    #plt.subplot(211)
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax.set_axis_off()

    ind = np.arange(25)
    width = 0.2

    h_group = ax1.bar(ind, hemingway.values()[:25], width, color='r')
    s_group = ax1.bar(ind+width, steinbeck.values()[:25], color='g', width=width)
    n_group = ax1.bar(ind+(2*width), nabokov.values()[:25], color='y', width=width)
    w_group = ax1.bar(ind+(3*width), wallace.values()[:25], color='b', width=width)

    ax1.legend((h_group[0], s_group[0], n_group[0], w_group[0]), ('hemingway', 'steinbeck', 'nabokov', 'wallace'))

    ax1.set_xticks(ind+(4/2*width))
    ax1.set_xticklabels(hemingway.keys()[:25], rotation='vertical')
    ax1.set_ylim([0, 0.2])

    ind2 = np.arange(26)
    h_group = ax2.bar(ind2, hemingway.values()[25:], width, color='r')
    s_group = ax2.bar(ind2+width, steinbeck.values()[25:], color='g', width=width)
    n_group = ax2.bar(ind2+(2*width), nabokov.values()[25:], color='y', width=width)
    w_group = ax2.bar(ind2+(3*width), wallace.values()[25:], color='b', width=width)


    ax2.set_xticks(ind2+(4/2*width))
    ax2.set_xticklabels(hemingway.keys()[25:], rotation='vertical')
    ax2.set_ylim([0, 0.2])

    ax2.legend((h_group[0], s_group[0], n_group[0], w_group[0]), ('hemingway', 'steinbeck', 'nabokov', 'wallace'))
    plt.show()

def plot_test(train, test):

    fig = plt.figure()
    #plt.subplot(211)
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax.set_axis_off()

    ind = np.arange(25)
    width = 0.33

    h_group = ax1.bar(ind, train.values()[:25], width, color='r')
    s_group = ax1.bar(ind+width, test.values()[:25], color='g', width=width)

    ax1.legend((h_group[0], s_group[0]), ('train', 'test'))

    ax1.set_xticks(ind+(2/2*width))
    ax1.set_xticklabels(train.keys()[:25], rotation='vertical')
    ax1.set_ylim([0, 0.11])

    ind2 = np.arange(26)
    h_group = ax2.bar(ind2, train.values()[25:], width, color='r')
    s_group = ax2.bar(ind2+width, test.values()[25:], color='g', width=width)


    ax2.set_xticks(ind+(2/2*width))
    ax2.set_xticklabels(train.keys()[25:], rotation='vertical')
    ax2.set_ylim([0, 0.11])

    ax2.legend((h_group[0], s_group[0]), ('train', 'test'))
    plt.show()

def find_function_words_text():
    """
    word_list = ['the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                 'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                 'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                 'can', 'some', 'their', 'over', 'down', 'your', 'will']
    """

    word_list = ['the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                 'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                 'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                 'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                 'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                 'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                 'another', 'myself']

    occurrences = defaultdict(int)

    with open('function_counts.txt') as infile:
        for line in infile:
            filename, tuple_list = line.split('\t')
            tuple_line = ast.literal_eval(tuple_list)
            for word, count in tuple_line:
                if word in word_list:
                    if filename in occurrences:
                        occurrences[filename].append((word, count))
                    else:
                        occurrences[filename]=[]
                        occurrences[filename].append((word, count))

    test_occurrences = defaultdict(int)
    with open('function_test_counts.txt') as infile:
        for line in infile:
            filename, tuple_list = line.split('\t')
            tuple_line = ast.literal_eval(tuple_list)
            for word, count in tuple_line:
                if word in word_list:
                    if filename in test_occurrences:
                        test_occurrences[filename].append((word, count))
                    else:
                        test_occurrences[filename]=[]
                        test_occurrences[filename].append((word, count))

    sorted_occurences = sorted(occurrences)
    sorted_test_occurrences = sorted(test_occurrences)

    hemingway = sorted_occurences[:12]
    nabokov = sorted_occurences[12:34]
    steinbeck = sorted_occurences[34:48]
    wallace = sorted_occurences[48:]
    hemingway_test = sorted_test_occurrences[:18]
    welch_test = sorted_test_occurrences[30]

    hemingway_avg=get_avg(occurrences, hemingway)
    nabokov_avg = get_avg(occurrences, nabokov)
    steinbeck_avg = get_avg(occurrences, steinbeck)
    wallace_avg = get_avg(occurrences, wallace)
    hemingway_test_avg = get_avg(test_occurrences, hemingway_test)
    welch_test_avg = get_avg(test_occurrences, welch_test)

    plot(hemingway_avg, nabokov_avg, steinbeck_avg, wallace_avg)
    #plot_test(hemingway_avg, hemingway_test_avg)
    #plot_test(wallace_avg, welch_test_avg)

def function_words(input_filename):
    word_list = ['the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                 'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                 'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                 'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                 'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                 'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                 'another', 'myself']

    file_dict = {}

    with open('/Users/eilidhhendry/PycharmProjects/author-similarity/function_word_counts/function_test_counts.txt') as infile:
        for line in infile:
            filename, tuple_list = line.split('\t')
            if filename.strip() == input_filename:
                tuple_line = ast.literal_eval(tuple_list)
                for word, count in tuple_line:
                    if word in word_list:
                        file_dict[word] = count
    result = []
    for word in word_list:
        if word in file_dict:
            result.append(file_dict[word])
        else:
            result.append(0)

    return result


def get_avg(occurences, file_list):
    result=defaultdict(int)
    word_count = 0
    for filename, tuple_list in occurences.items():
        if filename in file_list:
            for word, count in tuple_list:
                result[word]+=count
                word_count += count
    for word, count in result.items():
        result[word] = float(count)/word_count
    return result



if __name__=='__main__':
    #get_freqdist()
    find_function_words_text()
    #print function_words('hemingway/acrosstheriverandintothetrees.txt')
