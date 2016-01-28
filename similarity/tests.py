from django.test import TestCase
from classifier.compute_fingerprint import avg_syllables

# Create your tests here.
class SyllableTest(TestCase):
    def setUp(self):
        pass

    def test_no_syllables_in_string(self):
        test_sentence = "the quick brown fox jumped over the lazy dog"
        syllables_freq = avg_syllables(test_sentence.split())
        probably_right = 11.0/9
        self.assertEqual(syllables_freq, probably_right)

    def test_no_syllables_in_empty_string(self):
        test_sentence = ""
        syllables_freq = avg_syllables(test_sentence.split())
        probably_right = 0.0
        self.assertEqual(syllables_freq, probably_right)

    def test_no_syllables_in_arbitrary_words(self):
        test_sentence = "floogly rhombile shanaynord"
        syllables_freq = avg_syllables(test_sentence.split())
        probably_right = 0.0
        self.assertEqual(syllables_freq, probably_right)
