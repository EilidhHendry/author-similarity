__author__ = 'eilidhhendry'

# Ensure our data path is correct whether running from this directory,
# or from the django app
import os
current = os.getcwd()
CLASSIFIER_ROOT = ""
if not("classifier" in current):
    CLASSIFIER_ROOT += "similarity/classifier/"

DATA_PATH = CLASSIFIER_ROOT + "data/"
PLAINTEXT_PATH = DATA_PATH + "texts/"

CHUNK_SIZE = 32000

MODEL_PATH = DATA_PATH + "model/model.pkl"

POS_TAG_CATEGORIES = {
'POS_TAG_VERB': ["VB_pos_relative_frequency",  "VBD_pos_relative_frequency",  "VBG_pos_relative_frequency",  "VBN_pos_relative_frequency",  "VBP_pos_relative_frequency",  "VBZ_pos_relative_frequency",  "MD_pos_relative_frequency"],
'POS_TAG_NOUN': ["NN_pos_relative_frequency",  "NNP_pos_relative_frequency",  "NNPS_pos_relative_frequency",  "NNS_pos_relative_frequency"],
'POS_TAG_ADJECTIVE': ["JJ_pos_relative_frequency",  "JJR_pos_relative_frequency",  "JJS_pos_relative_frequency"],
'POS_TAG_DETERMINER': ["DT_pos_relative_frequency",  "PDT_pos_relative_frequency",  "WDT_pos_relative_frequency"],
'POS_TAG_ADVERB': ["RB_pos_relative_frequency",  "RBR_pos_relative_frequency",  "WRB_pos_relative_frequency"],
'POS_TAG_PRONOUN': ["PRP_pos_relative_frequency",  "PRP_possessive_pos_relative_frequency",  "WP_pos_relative_frequency",  "WP_possessive_pos_relative_frequency",  "EX_pos_relative_frequency"],
'POS_TAG_PREPOSITION': ["TO_pos_relative_frequency"],
'POS_TAG_CONJUNCTION': ["CC_pos_relative_frequency"],
'POS_TAG_INTERJECTION': ["UH_pos_relative_frequency"]
}

CHUNK_MODEL_FINGERPRINT_FIELDS = ["avg_word_length", "avg_sentence_length", "lexical_diversity", "percentage_punctuation", "avg_word_length_syllables", "the_relative_frequency", "and_relative_frequency", "of_relative_frequency", "a_relative_frequency", "to_relative_frequency", "in_relative_frequency", "i_relative_frequency", "he_relative_frequency", "it_relative_frequency", "that_relative_frequency", "you_relative_frequency", "his_relative_frequency", "with_relative_frequency", "on_relative_frequency", "for_relative_frequency", "at_relative_frequency", "as_relative_frequency", "but_relative_frequency", "her_relative_frequency", "they_relative_frequency", "she_relative_frequency", "him_relative_frequency", "all_relative_frequency", "this_relative_frequency", "we_relative_frequency", "from_relative_frequency", "or_relative_frequency", "out_relative_frequency", "an_relative_frequency", "my_relative_frequency", "by_relative_frequency", "up_relative_frequency", "what_relative_frequency", "me_relative_frequency", "no_relative_frequency", "like_relative_frequency", "would_relative_frequency", "if_relative_frequency", "about_relative_frequency", "which_relative_frequency", "them_relative_frequency", "into_relative_frequency", "who_relative_frequency", "could_relative_frequency", "can_relative_frequency", "some_relative_frequency", "their_relative_frequency", "over_relative_frequency", "down_relative_frequency", "your_relative_frequency", "will_relative_frequency", "its_relative_frequency", "any_relative_frequency", "through_relative_frequency", "after_relative_frequency", "off_relative_frequency", "than_relative_frequency", "our_relative_frequency", "us_relative_frequency", "around_relative_frequency", "these_relative_frequency", "because_relative_frequency", "must_relative_frequency", "before_relative_frequency", "those_relative_frequency", "should_relative_frequency", "himself_relative_frequency", "both_relative_frequency", "against_relative_frequency", "may_relative_frequency", "might_relative_frequency", "shall_relative_frequency", "since_relative_frequency", "de_relative_frequency", "within_relative_frequency", "between_relative_frequency", "each_relative_frequency", "under_relative_frequency", "until_relative_frequency", "toward_relative_frequency", "another_relative_frequency", "myself_relative_frequency", "PRP_pos_relative_frequency", "VBG_pos_relative_frequency", "VBD_pos_relative_frequency", "VBN_pos_relative_frequency", "POS_pos_relative_frequency", "VBP_pos_relative_frequency", "WDT_pos_relative_frequency", "JJ_pos_relative_frequency", "WP_pos_relative_frequency", "VBZ_pos_relative_frequency", "DT_pos_relative_frequency", "RP_pos_relative_frequency", "NN_pos_relative_frequency", "FW_pos_relative_frequency", "TO_pos_relative_frequency", "PRP_possessive_pos_relative_frequency", "RB_pos_relative_frequency", "NNS_pos_relative_frequency", "NNP_pos_relative_frequency", "VB_pos_relative_frequency", "WRB_pos_relative_frequency", "CC_pos_relative_frequency", "LS_pos_relative_frequency", "PDT_pos_relative_frequency", "RBS_pos_relative_frequency", "RBR_pos_relative_frequency", "CD_pos_relative_frequency", "EX_pos_relative_frequency", "IN_pos_relative_frequency", "WP_possessive_pos_relative_frequency", "MD_pos_relative_frequency", "NNPS_pos_relative_frequency", "JJS_pos_relative_frequency", "JJR_pos_relative_frequency", "UH_pos_relative_frequency"]
CONDENSED_FINGERPRINT_FIELDS = ["avg_word_length", "avg_sentence_length", "lexical_diversity", "percentage_punctuation", "avg_word_length_syllables", "POS_TAG_VERB", "POS_TAG_NOUN", "POS_TAG_ADJECTIVE", "POS_TAG_DETERMINER", "POS_TAG_ADVERB", "POS_TAG_PRONOUN", "POS_TAG_PREPOSITION", "POS_TAG_CONJUNCTION", "POS_TAG_INTERJECTION"]
