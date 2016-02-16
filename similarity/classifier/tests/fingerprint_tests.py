import unittest

import similarity.classifier.compute_fingerprint as compute_fingerprint

class FingerprintTest(unittest.TestCase):


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
            avg_word_length, _, _, _ = compute_fingerprint.analyze_text_string(test_sentence)
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
            _, avg_sentence_length, _, _ = compute_fingerprint.analyze_text_string(test_sentence)
            self.assertEquals(avg_sentence_length, result, msg=(test_sentence, avg_sentence_length, '!=', result))

    def test_lexical_diversity(self):
        test_sentences = [
            ("The quick brown cat jumped over the lazy dog.", float(8)/9),
            ("", 0),
            (".", 0),
            (" ", 0)
        ]
        for test_sentence, result in test_sentences:
            _, _, lexical_diversity, _ = compute_fingerprint.analyze_text_string(test_sentence)
            self.assertEquals(lexical_diversity, result, msg=(test_sentence, lexical_diversity, '!=', result))

    def test_percentage_punctuation(self):
        test_sentences = [
            ("The cat sat on the hat.", float(1)/18),
            (".", 1),
            (" ", 0),
        ]
        for test_sentence, result in test_sentences:
            _, _, _, percent_punctuation = compute_fingerprint.analyze_text_string(test_sentence)
            self.assertEquals(percent_punctuation, result, msg=(test_sentence, percent_punctuation, '!=', result))

    def test_avg_syllables(self):
        test_sentences = [
            ("The cat sat on the hat.", 1),
            (".", 0),
            (" ", 0),
            ("'Hi, my name is Kate'", 1)
        ]
        for test_sentence, result in test_sentences:
            avg_syllables = compute_fingerprint.avg_syllables(test_sentence)
            print avg_syllables
            self.assertEquals(avg_syllables, result, msg=(test_sentence, avg_syllables, '!=', result))

if __name__ == '__main__':
    unittest.main()