import constants
import os
import nltk
import regex

from util import tokenize_words, tokenize_sentences


pronounciation_dict = nltk.corpus.cmudict.dict()

def fingerprint_text(chunk):
    """
    :param chunk: takes input as string
    :return: list containing author name plus floats representing fingerprint
    """

    # dictionary to return calculated fingerprints
    results = {key: 0 for key in constants.CHUNK_MODEL_FINGERPRINT_FIELDS}

    # tokenise the input text
    words = tokenize_words(chunk)

    # find the length of the current chunk, if 0 return all 0s
    if len(words) == 0: return results

    # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
    # store results in dictionary
    analyse_text_results = analyze_text(chunk)

    for field_name in analyse_text_results.keys():
        if field_name in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
            results[field_name]=analyse_text_results[field_name]

    if 'avg_word_length_syllables' in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
        # get avg num syllables per word
        avg_syllables_result  = avg_syllables(words)
        results['avg_word_length_syllables'] = avg_syllables_result

    # find the function words in the list of fields
    function_word_list = get_function_word_list(constants.CHUNK_MODEL_FINGERPRINT_FIELDS)
    #find the pos tags in the list of fields
    tag_list = get_tag_list(constants.CHUNK_MODEL_FINGERPRINT_FIELDS)

    # only tag the text if finding function words or pos tags
    if function_word_list or tag_list:
        # tag current text
        # requires nltk maxent_treebank_tagger downloaded
        pos_current_text = nltk.pos_tag(words)

        # get normalised function word distributions
        function_word_distribution = get_function_word_distribution(pos_current_text, function_word_list)
        assert len(function_word_distribution) == len(function_word_list), \
        'there are %r fields in function_word_list, but function_word_distribution contains %r' \
        % (len(function_word_distribution), len(function_word_list))
        results.update(function_word_distribution)

        # get normalised pos distributions
        pos_distribution = get_pos_counts(pos_current_text, tag_list)
        assert len(pos_distribution) == len(tag_list), \
        'there are %r fields in tag_list, but pos_distribution contains %r' \
        % (len(tag_list), len(pos_distribution))

        results.update(pos_distribution)

    assert len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS) == len(results.keys()), \
        'there are %r fields in constants.CHUNK_MODEL_FINGERPRINT_FIELDS, but results contain %r' \
        % (len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS), len(results.keys()))

    return results


def analyze_text(input_chunk):
        results = {key: 0 for key in
                   ['avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation']}

        chars = ''.join(input_chunk.split())
        chars_without_punc = remove_punctuation(chars)
        words = tokenize_words(input_chunk)
        words_without_punc = [word for word in words if remove_punctuation(word)]
        sentences = tokenize_sentences(input_chunk)

        word_count = len(words_without_punc)
        char_count_with_punc = len(chars)
        char_count_without_punc = len(chars_without_punc)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in words_without_punc))
        punctuation_count = len([char for char in chars if regex.match(ur"\p{P}+", char)])

        if word_count > 0:
            results['avg_word_length'] = float(char_count_without_punc)/word_count
            results['lexical_diversity'] = float(vocab_count) / word_count
        if sentence_count > 0:
            results['avg_sentence_length'] = float(word_count)/sentence_count
        if char_count_with_punc > 0:
            results['percentage_punctuation'] = float(punctuation_count) / char_count_with_punc

        return results

def remove_punctuation(text):
    return regex.sub(ur"\p{P}+", "", text)

def number_syllables(word):
    if word.lower() in pronounciation_dict:
        syllable_list = [len(list(phoneme for phoneme in phonemes if phoneme[-1].isdigit())) for phonemes in pronounciation_dict[word.lower()]]
        if len(set(syllable_list)) == 1:
            return syllable_list[0]
        else:
            return -1
    else:
        return -1


def avg_syllables(words):
    not_in_dictionary = 0
    syllable_list = []
    for word in words:
        clean_word = word.lower().strip()
        # ignore word if the word contains any punctuation or if digit
        if not regex.match(ur"\p{P}+", word) and not word.isdigit():
            syllables_in_word = number_syllables(clean_word)
            if syllables_in_word == -1:
                not_in_dictionary += 1
            else:
                syllable_list.append(syllables_in_word)
    if len(syllable_list) > 0:
        avg_num_syllables = float(sum(syllable_list))/len(syllable_list)
    else:
        avg_num_syllables = 0
    return avg_num_syllables


def get_tag_list(fingerprint_fields):
    tag_list = []
    tag_end = "_pos_relative_frequency"
    # if the field ends with "_pos_relative_frequency"
    # then remove that from end and add word to list
    for field in fingerprint_fields:
        if field.endswith(tag_end):
            tag = field.replace(tag_end, "")
            if tag.endswith("_possessive"):
                tag = tag.replace("_possessive", "$")
            tag_list.append(tag)
    return tag_list

def tag_to_field(tag):
    if tag.endswith('$'):
        tag = tag.replace('$', "_possessive")
    tag+='_pos_relative_frequency'
    return tag

def get_pos_counts(tagged_text, tag_list):
    # TODO: check should be normalised by no. words or no. tags; get rid of text length

    # initialise dictionary with tag list as keys
    final_pos_distribution = {tag_to_field(key): 0 for key in tag_list}

    length_tagged_text = len([word for (word, tag) in tagged_text if not regex.match(ur"\p{P}+", word)])
    if length_tagged_text == 0: return final_pos_distribution

    # create frequency distribution of tags in text
    tagged_text_freq_dist = nltk.FreqDist(tag for (word, tag) in tagged_text)

    # loop through the frequency distribution dictionary, normalise and add to empty but initialised dictionary of tags
    # this approach preserves 0 values for tags which do not occur in current text
    for tag, count in tagged_text_freq_dist.iteritems():
        if tag in tag_list:
            final_pos_distribution[tag_to_field(tag)] = float(count)/length_tagged_text

    return final_pos_distribution


def get_function_word_list(fingerprint_fields):
    function_word_list = []
    function_end = "_relative_frequency"
    # if the field ends with "_relative_frequency" and doesn't contain pos
    # then remove that from end and add word to list
    for field in fingerprint_fields:
        if 'pos' not in field and field.endswith(function_end):
            function_word = field.replace(function_end, "")
            function_word_list.append(function_word)
    return function_word_list


def get_function_word_distribution(tagged_text, word_list):
    # TODO: check normalised by no. words or no. tags; get rid of text_length
    taglist = 'PRP PRP$ WP WP$ CC MD UH RP IN TO WDT DT PDT'.split()

    # initialise dictionary with word list as keys
    word_list_dict = {key+'_relative_frequency': 0 for key in word_list}

    length_tagged_text = len([word for (word, tag) in tagged_text if not regex.match(ur"\p{P}+", word)])
    if length_tagged_text == 0: return word_list_dict

    word_fd = nltk.FreqDist(word.lower() for (word, tag) in tagged_text if tag in taglist)

    for word, count in word_fd.iteritems():
        if word in word_list:
            word_list_dict[word+'_relative_frequency'] = float(count)/length_tagged_text

    return word_list_dict
