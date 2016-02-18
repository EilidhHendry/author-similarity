import unittest

import similarity.classifier.constants as constants
import similarity.classifier.compute_fingerprint as compute_fingerprint

class FingerprintTest(unittest.TestCase):
    # TODO: tokenize tests, pos tests, function word tests, more test sentences for avg syllables

    def setUp(self):
        pass

    def test_average_word_length(self):
        avg_word_length_cases = [
            ("The quick brown cat jumped over the lazy dog", 4),
            ("", 0),
            (" ", 0),
            (",", 0)
        ]
        for test_sentence, result in avg_word_length_cases:
            avg_word_length, _, _, _ = compute_fingerprint.analyze_text(test_sentence)
            self.assertEquals(avg_word_length, result, msg=(test_sentence, avg_word_length, '!=', result))

    def test_average_sentence_length(self):
        avg_sentence_length_cases = [
            ("The cat sat on the hat. The fox jumped.", 4.5),
            ("", 0),
            ("Alice.", 1),
            ("Mr. Smith went to work.", 5),
            ("'hi,' said Katie.", 3)
        ]
        for test_sentence, result in avg_sentence_length_cases:
            _, avg_sentence_length, _, _ = compute_fingerprint.analyze_text(test_sentence)
            self.assertEquals(avg_sentence_length, result, msg=(test_sentence, avg_sentence_length, '!=', result))

    def test_lexical_diversity(self):
        test_sentences = [
            ("The quick brown cat jumped over the lazy dog.", float(8)/9),
            ("", 0),
            (".", 0),
            (" ", 0)
        ]
        for test_sentence, result in test_sentences:
            _, _, lexical_diversity, _ = compute_fingerprint.analyze_text(test_sentence)
            self.assertEquals(lexical_diversity, result, msg=(test_sentence, lexical_diversity, '!=', result))

    def test_percentage_punctuation(self):
        test_sentences = [
            ("The cat sat on the hat.", float(1)/18),
            (".", 1),
            (" ", 0),
            ("", 0)
        ]
        for test_sentence, result in test_sentences:
            _, _, _, percent_punctuation = compute_fingerprint.analyze_text(test_sentence)
            self.assertEquals(percent_punctuation, result, msg=(test_sentence, percent_punctuation, '!=', result))

    def test_avg_syllables(self):
        test_sentences = [
            ("The cat sat on the hat.", 1),
            (".", 0),
            (" ", 0),
            ("'Hi, my name is Kate'", 1),
            ("", 0)
        ]
        for test_sentence, result in test_sentences:
            avg_syllables = compute_fingerprint.avg_syllables(test_sentence)
            self.assertEquals(avg_syllables, result, msg=(test_sentence, avg_syllables, '!=', result))

    def test_pos_distribution(self):
        # TODO: more sentences
        test_sentences = [
            ([("dog", "NN")], [1, 0, 0]),
            ([], [0, 0, 0]),
            ([('the', 'DT'), ('quick', 'NN'), ('brown', 'NN'), ('fox', 'NN'), ('jumped', 'VBD'), ('.', '.')],
             [0.5, float(1)/6, float(1)/6])
        ]
        tag_list = ["NN", "DT", "VBD"]
        for tagged_test_sentence, result in test_sentences:
            pos_freq_dis = compute_fingerprint.get_pos_counts(tagged_test_sentence, len(tagged_test_sentence), tag_list)
            self.assertEquals(pos_freq_dis, result, msg=(tagged_test_sentence, pos_freq_dis, '!=', result))

    def test_function_word_distribution(self):
        # TODO: more sentences
        test_sentences = [
            ([("into", "IN"), ("the", "DET"), ("dog", "NN")], [float(1)/3]),
            ([], [0])
        ]
        tag_list = ["into"]
        for tagged_test_sentence, result in test_sentences:
            function_word_dist = compute_fingerprint.get_function_word_distribution(tagged_test_sentence, len(tagged_test_sentence), tag_list)
            self.assertEquals(function_word_dist, result, msg=(tagged_test_sentence, function_word_dist, '!=', result))


    def test_fingerprint_text(self):
        test_texts = [
            ({'author_name': 'test_author',
            'book_title': 'test_book',
            'input_chunk_or_path': '',
            'from_file': False},
             ['test_author'] + [0 for field in constants.CHUNK_MODEL_FINGERPRINT_FIELDS])
             ]

        for dictionary, result in test_texts:
            fingerprint = compute_fingerprint.fingerprint_text_string(
                dictionary['author_name'], dictionary['book_title'], dictionary['input_chunk_or_path'],
                write_to_csv=False, from_file=dictionary['from_file'])
            self.assertEquals(fingerprint, result)

if __name__ == '__main__':
    unittest.main()