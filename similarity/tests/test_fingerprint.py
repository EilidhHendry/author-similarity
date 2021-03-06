#!/usr/bin/env python2.7
import unittest
import nltk
import codecs

import similarity.classifier.constants as constants
import similarity.classifier.compute_fingerprint as compute_fingerprint
import similarity.classifier.chunk as chunk
import similarity.classifier.util as util

from similarity.tests.test_data.seuss_test_results import seuss_result_dictionary

test_text = "I am Sam. I am Sam. Sam-I-Am. \n" \
            "That Sam-I-Am! That Sam-I-Am! I do not like that Sam-I-Am! \n" \
            "Do you like green eggs and ham? \n" \
            "I do not like them, Sam-I-Am. \n" \
            "I do not like green eggs and ham."

class FingerprintTest(unittest.TestCase):
    # TODO: tokenize tests, pos tests, function word tests, more test sentences for avg syllables

    def setUp(self):
        pass

    def test_tokenise_words(self):
        test_sentences = [
            ('', []),
            (' ', []),
            ("I don't like it. You'll agree?", ["I", "don", "'", "t", "like", "it", ".", "You", "'", "ll", "agree", "?"]),
            (test_text,
             ['I', 'am', 'Sam', '.', 'I', 'am', 'Sam', '.', 'Sam', '-', 'I', '-', 'Am', '.',
              'That', 'Sam', '-', 'I', '-', 'Am', '!', 'That', 'Sam', '-', 'I', '-', 'Am', '!',
              'I', 'do', 'not', 'like', 'that', 'Sam', '-', 'I', '-', 'Am', '!',
              'Do', 'you', 'like', 'green', 'eggs', 'and', 'ham', '?',
              'I', 'do', 'not', 'like', 'them', ',', 'Sam', '-', 'I', '-', 'Am', '.',
              'I', 'do', 'not', 'like', 'green', 'eggs', 'and', 'ham', '.'])
        ]
        for test_sentence, result in test_sentences:
            tokens = util.tokenize_words(test_sentence)
            self.assertEquals(tokens, result, msg=(test_sentence, tokens, '!=', result))

    def test_average_word_length(self):
        avg_word_length_cases = [
            ("The quick brown fox jumped over the lazy dog", 4),
            ("", 0),
            (" ", 0),
            (",", 0),
            (test_text, 127.0/48)
        ]
        for test_sentence, result in avg_word_length_cases:
            analyse_result_dict = compute_fingerprint.analyze_text(util.tokenize_sentences(test_sentence))
            avg_word_length = analyse_result_dict['avg_word_length']
            self.assertEquals(avg_word_length, result, msg=(test_sentence, avg_word_length, '!=', result))

    def test_average_sentence_length(self):
        avg_sentence_length_cases = [
            ("The cat sat on the hat. The fox jumped.", 4.5),
            ("", 0),
            ("Alice.", 1),
            ("Mr. Smith went to work.", 5),
            ("'hi,' said Katie.", 3),
            (test_text, 48.0/9)
        ]
        for test_sentence, result in avg_sentence_length_cases:
            analyse_result_dict = compute_fingerprint.analyze_text(util.tokenize_sentences(test_sentence))
            avg_sentence_length = analyse_result_dict['avg_sentence_length']
            self.assertEquals(avg_sentence_length, result, msg=(test_sentence, avg_sentence_length, '!=', result))

    def test_lexical_diversity(self):
        test_sentences = [
            ("The quick brown cat jumped over the lazy dog.", float(8)/9),
            ("", 0),
            (".", 0),
            (" ", 0),
            (test_text, 13.0/48)
        ]
        for test_sentence, result in test_sentences:
            analyse_result_dict = compute_fingerprint.analyze_text(util.tokenize_sentences(test_sentence))
            lexical_diversity = analyse_result_dict['lexical_diversity']
            self.assertEquals(lexical_diversity, result, msg=(test_sentence, lexical_diversity, '!=', result))

    def test_percentage_punctuation(self):
        test_sentences = [
            ("The cat sat on the hat.", float(1)/18),
            (".", 1),
            (" ", 0),
            ("", 0),
            (test_text, 20.0/147)
        ]
        for test_sentence, result in test_sentences:
            analyse_result_dict = compute_fingerprint.analyze_text(util.tokenize_sentences(test_sentence))
            percent_punctuation = analyse_result_dict['percentage_punctuation']
            self.assertEquals(percent_punctuation, result, msg=(test_sentence, percent_punctuation, '!=', result))

    def test_avg_syllables(self):
        test_sentences = [
            ("The cat sat on the hat.", 1),
            (".", 0),
            (" ", 0),
            ("'Hi, my name is Kate'", 1),
            ("", 0),
            (test_text, 1.0)
        ]
        for test_sentence, result in test_sentences:
            avg_syllables = compute_fingerprint.avg_syllables(test_sentence)
            self.assertEquals(avg_syllables, result, msg=(test_sentence, avg_syllables, '!=', result))

    def test_pos_distribution(self):
        # TODO: more sentences
        tag_list = ["NN", "DT", "VBD", "PRP", "VBP", "RB", "IN", "NNS", "CC", "NNP", "JJ", "VB"]
        test_sentences = [
            ("dog",
             {key+"_pos_relative_frequency": 0 if key is not "NN" else 1.0 for key in tag_list}),
            ('', {key+"_pos_relative_frequency": 0 for key in tag_list}),
            ('the quick brown fox jumped.',
             {"PRP_pos_relative_frequency": 0,
              "NN_pos_relative_frequency": 2.0/5,
              "DT_pos_relative_frequency": 1.0/5,
              "VBP_pos_relative_frequency": 0,
              "RB_pos_relative_frequency": 0,
              "IN_pos_relative_frequency": 0,
              "NNS_pos_relative_frequency": 0,
              "CC_pos_relative_frequency": 0,
              "NNP_pos_relative_frequency": 0,
              "JJ_pos_relative_frequency": 1.0/5,
              "VB_pos_relative_frequency": 0,
              "VBD_pos_relative_frequency": 1.0/5}),
            (test_text,
             {"PRP_pos_relative_frequency": 12.0/48,
              "NN_pos_relative_frequency": 5.0/48,
              "DT_pos_relative_frequency": 3.0/48,
              "VBP_pos_relative_frequency": 8.0/48,
              "RB_pos_relative_frequency": 3.0/48,
              "IN_pos_relative_frequency": 3.0/48,
              "NNS_pos_relative_frequency": 2.0/48,
              "CC_pos_relative_frequency": 2.0/48,
              "NNP_pos_relative_frequency": 7.0/48,
              "JJ_pos_relative_frequency": 2.0/48,
              "VB_pos_relative_frequency": 1.0/48,
              "VBD_pos_relative_frequency": 0})
        ]
        for test_sentence, result in test_sentences:
            pos_freq_dis = compute_fingerprint.get_pos_counts(nltk.pos_tag(util.tokenize_words(test_sentence)), tag_list)
            print
            self.assertEquals(pos_freq_dis, result, msg=(test_sentence, pos_freq_dis, '!=', result))

    def test_function_word_distribution(self):
        # TODO: more sentences
        test_sentences = [
            ("into the dog",
             {"into_relative_frequency": 1.0/3,
                  "i_relative_frequency": 0,
                  "that_relative_frequency": 0,
                  "like_relative_frequency": 0,
                  "you_relative_frequency": 0,
                  "and_relative_frequency": 0,
                  "them_relative_frequency": 0}),
            ('', {"into_relative_frequency": 0,
                  "i_relative_frequency": 0,
                  "that_relative_frequency": 0,
                  "like_relative_frequency": 0,
                  "you_relative_frequency": 0,
                  "and_relative_frequency": 0,
                  "them_relative_frequency": 0}),
            (test_text, {
                "into_relative_frequency": 0,
                "i_relative_frequency": 10.0/48,
                "that_relative_frequency": 3.0/48,
                "like_relative_frequency": 3.0/48,
                "you_relative_frequency": 1.0/48,
                "and_relative_frequency": 2.0/48,
                "them_relative_frequency": 1.0/48})
        ]
        tag_list = ["into", "i", "that", "like", "you", "and", "them"]
        for test_sentence, result in test_sentences:
            function_word_dist = compute_fingerprint.get_function_word_distribution(nltk.pos_tag(util.tokenize_words(test_sentence)), tag_list)
            self.assertEquals(function_word_dist, result, msg=(test_sentence, function_word_dist, '!=', result))

    def test_fingerprint_text(self):
        empty_result = {key: 0 for key in constants.CHUNK_MODEL_FINGERPRINT_FIELDS}
        test_texts = [
            ({'chunk': ' '},
             empty_result),
            ({'chunk': test_text},
             seuss_result_dictionary)
            ]

        for argument_dictionary, result_dictionary in test_texts:
            result_list = []
            fingerprint_list=[]

            fingerprint = compute_fingerprint.fingerprint_text(util.tokenize_sentences(argument_dictionary['chunk']))
            for field in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
                result_list.append(result_dictionary[field])
                fingerprint_list.append(fingerprint[field])
            self.assertEquals(fingerprint_list, result_list)

    def test_fingerprint_chunk_integration(self):
        fingerprints = []
        for text_chunk in chunk.chunk_text('similarity/tests/test_data/seuss_test_book.txt'):
            fingerprints.append(compute_fingerprint.fingerprint_text(text_chunk))
        result_dict = {key: 0 for key in constants.CHUNK_MODEL_FINGERPRINT_FIELDS}
        for fingerprint in fingerprints:
            for key, value in fingerprint.items():
                result_dict[key]+=value
        self.assertEquals(result_dict, seuss_result_dictionary)
