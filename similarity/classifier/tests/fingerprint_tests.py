import unittest
import nltk

import similarity.classifier.constants as constants
import similarity.classifier.compute_fingerprint as compute_fingerprint


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
            tokens = compute_fingerprint.tokenize_words(test_sentence)
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
            analyse_result_dict = compute_fingerprint.analyze_text(test_sentence)
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
            analyse_result_dict = compute_fingerprint.analyze_text(test_sentence)
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
            analyse_result_dict = compute_fingerprint.analyze_text(test_sentence)
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
            analyse_result_dict = compute_fingerprint.analyze_text(test_sentence)
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
            ([("dog", "NN")],
             {key+"_pos_relative_frequency": 0 if key is not "NN" else 1.0 for key in tag_list}),
            ([], {key+"_pos_relative_frequency": 0 for key in tag_list}),
            ([('the', 'DT'), ('quick', 'NN'), ('brown', 'NN'), ('fox', 'NN'), ('jumped', 'VBD'), ('.', '.')],
             {"PRP_pos_relative_frequency": 0,
              "NN_pos_relative_frequency": 3.0/5,
              "DT_pos_relative_frequency": 1.0/5,
              "VBP_pos_relative_frequency": 0,
              "RB_pos_relative_frequency": 0,
              "IN_pos_relative_frequency": 0,
              "NNS_pos_relative_frequency": 0,
              "CC_pos_relative_frequency": 0,
              "NNP_pos_relative_frequency": 0,
              "JJ_pos_relative_frequency": 0,
              "VB_pos_relative_frequency": 0,
              "VBD_pos_relative_frequency": 1.0/5}),
            (nltk.pos_tag(compute_fingerprint.tokenize_words(test_text)),
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
        for tagged_test_sentence, result in test_sentences:
            pos_freq_dis = compute_fingerprint.get_pos_counts(tagged_test_sentence, tag_list)
            self.assertEquals(pos_freq_dis, result, msg=(tagged_test_sentence, pos_freq_dis, '!=', result))

    def test_function_word_distribution(self):
        # TODO: more sentences
        test_sentences = [
            ([("into", "IN"), ("the", "DET"), ("dog", "NN")],
             {"into_relative_frequency": 1.0/3,
                  "i_relative_frequency": 0,
                  "that_relative_frequency": 0,
                  "like_relative_frequency": 0,
                  "you_relative_frequency": 0,
                  "and_relative_frequency": 0,
                  "them_relative_frequency": 0}),
            ([], {"into_relative_frequency": 0,
                  "i_relative_frequency": 0,
                  "that_relative_frequency": 0,
                  "like_relative_frequency": 0,
                  "you_relative_frequency": 0,
                  "and_relative_frequency": 0,
                  "them_relative_frequency": 0}),
            (nltk.pos_tag(compute_fingerprint.tokenize_words(test_text)), {
                "into_relative_frequency": 0,
                "i_relative_frequency": 10.0/48,
                "that_relative_frequency": 3.0/48,
                "like_relative_frequency": 3.0/48,
                "you_relative_frequency": 1.0/48,
                "and_relative_frequency": 2.0/48,
                "them_relative_frequency": 1.0/48})
        ]
        tag_list = ["into", "i", "that", "like", "you", "and", "them"]
        for tagged_test_sentence, result in test_sentences:
            function_word_dist = compute_fingerprint.get_function_word_distribution(tagged_test_sentence, tag_list)
            self.assertEquals(function_word_dist, result, msg=(tagged_test_sentence, function_word_dist, '!=', result))

    def test_fingerprint_text(self):
        author_name = 'test_author'
        empty_result = {key: 0 for key in constants.CHUNK_MODEL_FINGERPRINT_FIELDS}
        empty_result['author_name']=author_name
        test_texts = [
            ({'author_name': author_name,
              'book_title': 'test_book',
              'chunk_name': 'chunk_name',
              'chunk_as_string': ' ',
              'chunk_as_path': None},
             empty_result),
            ({'author_name': author_name,
              'book_title': 'test_book',
              'chunk_name': 'chunk_name',
              'chunk_as_string': test_text,
              'chunk_as_path': None},
             {"author_name": author_name,
              "avg_word_length": 127.0/48,
              "avg_sentence_length": 48.0/9,
              "lexical_diversity": 13.0/48,
              "percentage_punctuation": 20.0/147,
              "avg_word_length_syllables": 1.0,
              "the_relative_frequency": 0,
              "and_relative_frequency": 2.0/48,
              "of_relative_frequency": 0,
              "a_relative_frequency": 0,
              "to_relative_frequency": 0,
              "in_relative_frequency": 0,
              "i_relative_frequency": 10.0/48,
              "he_relative_frequency": 0,
              "it_relative_frequency": 0,
              "that_relative_frequency": 3.0/48,
              "you_relative_frequency": 1.0/48,
              "his_relative_frequency": 0,
              "with_relative_frequency": 0,
              "on_relative_frequency": 0,
              "for_relative_frequency": 0,
              "at_relative_frequency": 0,
              "as_relative_frequency": 0,
              "but_relative_frequency": 0,
              "her_relative_frequency": 0,
              "they_relative_frequency": 0,
              "she_relative_frequency": 0,
              "him_relative_frequency": 0,
              "all_relative_frequency": 0,
              "this_relative_frequency": 0,
              "we_relative_frequency": 0,
              "from_relative_frequency": 0,
              "or_relative_frequency": 0,
              "out_relative_frequency": 0,
              "an_relative_frequency": 0,
              "my_relative_frequency": 0,
              "by_relative_frequency": 0,
              "up_relative_frequency": 0,
              "what_relative_frequency": 0,
              "me_relative_frequency": 0,
              "no_relative_frequency": 0,
              "like_relative_frequency": 3.0/48,
              "would_relative_frequency": 0,
              "if_relative_frequency": 0,
              "about_relative_frequency": 0,
              "which_relative_frequency": 0,
              "them_relative_frequency": 1.0/48,
              "into_relative_frequency": 0,
              "who_relative_frequency": 0,
              "could_relative_frequency": 0,
              "can_relative_frequency": 0,
              "some_relative_frequency": 0,
              "their_relative_frequency": 0,
              "over_relative_frequency": 0,
              "down_relative_frequency": 0,
              "your_relative_frequency": 0,
              "will_relative_frequency": 0,
              "its_relative_frequency": 0,
              "any_relative_frequency": 0,
              "through_relative_frequency": 0,
              "after_relative_frequency": 0,
              "off_relative_frequency": 0,
              "than_relative_frequency": 0,
              "our_relative_frequency": 0,
              "us_relative_frequency": 0,
              "around_relative_frequency": 0,
              "these_relative_frequency": 0,
              "because_relative_frequency": 0,
              "must_relative_frequency": 0,
              "before_relative_frequency": 0,
              "those_relative_frequency": 0,
              "should_relative_frequency": 0,
              "himself_relative_frequency": 0,
              "both_relative_frequency": 0,
              "against_relative_frequency": 0,
              "may_relative_frequency": 0,
              "might_relative_frequency": 0,
              "shall_relative_frequency": 0,
              "since_relative_frequency": 0,
              "de_relative_frequency": 0,
              "within_relative_frequency": 0,
              "between_relative_frequency": 0,
              "each_relative_frequency": 0,
              "under_relative_frequency": 0,
              "until_relative_frequency": 0,
              "toward_relative_frequency": 0,
              "another_relative_frequency": 0,
              "myself_relative_frequency": 0,
              "PRP_pos_relative_frequency": 12.0/48,
              "VBG_pos_relative_frequency": 0,
              "VBD_pos_relative_frequency": 0,
              "VBN_pos_relative_frequency": 0,
              "POS_pos_relative_frequency": 0,
              "VBP_pos_relative_frequency": 8.0/48,
              "WDT_pos_relative_frequency": 0,
              "JJ_pos_relative_frequency": 2.0/48,
              "WP_pos_relative_frequency": 0,
              "VBZ_pos_relative_frequency": 0,
              "DT_pos_relative_frequency": 3.0/48,
              "RP_pos_relative_frequency": 0,
              "NN_pos_relative_frequency": 5.0/48,
              "FW_pos_relative_frequency": 0,
              "TO_pos_relative_frequency": 0,
              "PRP_dollar_pos_relative_frequency": 0,
              "RB_pos_relative_frequency": 3.0/48,
              "NNS_pos_relative_frequency": 2.0/48,
              "NNP_pos_relative_frequency": 7.0/48,
              "VB_pos_relative_frequency": 1.0/48,
              "WRB_pos_relative_frequency": 0,
              "CC_pos_relative_frequency": 2.0/48,
              "LS_pos_relative_frequency": 0,
              "PDT_pos_relative_frequency": 0,
              "RBS_pos_relative_frequency": 0,
              "RBR_pos_relative_frequency": 0,
              "CD_pos_relative_frequency": 0,
              "EX_pos_relative_frequency": 0,
              "IN_pos_relative_frequency": 3.0/48,
              "WP_dollar_pos_relative_frequency": 0,
              "MD_pos_relative_frequency": 0,
              "NNPS_pos_relative_frequency": 0,
              "JJS_pos_relative_frequency" : 0,
              "JJR_pos_relative_frequency" : 0,
              "UH_pos_relative_frequency": 0})
            ]

        for argument_dictionary, result_dictionary in test_texts:
            result_list = []
            fingerprint_list=[]

            fingerprint = compute_fingerprint.fingerprint_text_string(
                argument_dictionary['author_name'], argument_dictionary['book_title'], argument_dictionary['chunk_name'],
                write_to_csv=False, chunk_as_string=argument_dictionary['chunk_as_string'],
                chunk_as_path=argument_dictionary['chunk_as_path'])
            for field in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
                result_list.append(result_dictionary[field])
                fingerprint_list.append(fingerprint[field])
            self.assertEquals(fingerprint_list, result_list)

if __name__ == '__main__':
    unittest.main()
