import constants
import os
import nltk
import csv
import string


pronounciation_dict = nltk.corpus.cmudict.dict()
punctuation_marks = ['!', ',', '.', ':', '"', '\'', '?', '-', ';', '(', ')', '[', ']', '\\', '/', '`']

def fingerprint_text(author_name, book_title, chunk_name, write_to_csv=True, chunk_as_path=None, chunk_as_string=None):
    """
    Can take a text as either a string or a path to file
    :param write_to_csv: if true writes results to csv
    :param chunk_as_path: if not None tries to read input_chunk_or_path as file
    :param chunk_as_string: if not None takes input as string
    :return: list containing author name plus floats representing fingerprint
    """
    #TODO: remove author_name, book_title and chunk_name (required for csv writing)

    if chunk_as_path:
        try:
            with open(chunk_as_path) as content_file:
                text_content = content_file.read()
        except IOError:
            print 'could not open file'
            raise
    elif chunk_as_string:
        text_content = chunk_as_string
    else:
        raise ValueError('Must provide values for either chunk_as_path or chunk_as_string')

    # dictionary to return calculated fingerprints
    results = {key: 0 for key in constants.CHUNK_MODEL_FINGERPRINT_FIELDS}

    # tokenise the input text
    words = tokenize_words(text_content)

    # find the length of the current chunk, if 0 return all 0s
    if len(words) == 0: return results

    # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
    # store results in dictionary
    analyse_text_results = analyze_text(text_content)

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

    if write_to_csv:
        fingerprint_to_csv(results, author_name, book_title, chunk_name)

    assert len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS) == len(results.keys()), \
        'there are %r fields in constants.CHUNK_MODEL_FINGERPRINT_FIELDS, but results contain %r' \
        % (len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS), len(results.keys()))

    return results

def tokenize_words(input_chunk):
    """
    Takes string and returns list of tokens
    :param input_chunk: string
    :return: list
    """
    word_tokenizer = nltk.tokenize.WordPunctTokenizer()
    return word_tokenizer.tokenize(input_chunk)


def tokenize_sentences(input_chunk):
    """
    Takes string and returns list of sentences containing lists of tokens
    :param input_chunk: string
    :return: list of lists
    """
    sentence_tokenizer=nltk.data.LazyLoader('tokenizers/punkt/english.pickle')
    return [tokenize_words(sentence) for sentence in sentence_tokenizer.tokenize(input_chunk)]


def fingerprint_to_csv(fingerprint_dictionary, author_name, book_title, chunk_name):
    # create csv writer object, output file and write headers to file
    csv_writer = create_csv(author_name, book_title, chunk_name)

    # loop through list of fields and append results in order
    ordered_fingerprint_list = [author_name]
    for field in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
        ordered_fingerprint_list.append(fingerprint_dictionary[field])

    # write list to csv file
    csv_writer.writerow(ordered_fingerprint_list)


def analyze_text(input_chunk):
        results = {key: 0 for key in
                   ['avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation']}

        chars = input_chunk.translate(None, string.whitespace)
        chars_without_punc = chars.translate(None, string.punctuation)
        words = tokenize_words(input_chunk)
        words_without_punc = [word for word in words if not set(word).intersection(set(string.punctuation))]
        sentences = tokenize_sentences(input_chunk)

        word_count = len(words_without_punc)
        char_count_with_punc = len(chars)
        char_count_without_punc = len(chars_without_punc)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in words_without_punc))
        punctuation_count = len([char for char in chars if set(char).intersection(set(punctuation_marks))])

        if word_count > 0:
            results['avg_word_length'] = float(char_count_without_punc)/word_count
            results['lexical_diversity'] = float(vocab_count) / word_count
        if sentence_count > 0:
            results['avg_sentence_length'] = float(word_count)/sentence_count
        if char_count_with_punc > 0:
            results['percentage_punctuation'] = float(punctuation_count) / char_count_with_punc

        return results


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
        if not set(word).intersection(set(punctuation_marks)) and not word.isdigit():
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
            if tag.endswith("_dollar"):
                tag = tag.replace("_dollar", "$")
            tag_list.append(tag)
    return tag_list

def tag_to_field(tag):
    if tag.endswith('$'):
        tag = tag.replace('$', "_dollar")
    tag+='_pos_relative_frequency'
    return tag

def get_pos_counts(tagged_text, tag_list):
    # TODO: check should be normalised by no. words or no. tags; get rid of text length

    # initialise dictionary with tag list as keys
    final_pos_distribution = {tag_to_field(key): 0 for key in tag_list}

    length_tagged_text = len([word for (word, tag) in tagged_text if word not in string.punctuation])
    if length_tagged_text == 0: return final_pos_distribution

    # create frequency distribution of tags in text
    tagged_text_freq_dist = nltk.FreqDist(tag for (word, tag) in tagged_text)

    # loop through the frequency distribution dictionary, normalise and add to empty but initialised dictionary of tags
    # this approach preserves 0 values for tags which do not occur in current text
    for tag, count in tagged_text_freq_dist.iteritems():
        if tag in tag_list:
            final_pos_distribution[tag_to_field(tag)] = float(count)/length_tagged_text

    # create list of results in order to preserve tag list ordering
    #ordered_pos_distributions = [final_pos_distribution[tag] for tag in tag_list]
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

    length_tagged_text = len([word for (word, tag) in tagged_text if word not in string.punctuation])
    if length_tagged_text == 0: return word_list_dict

    word_fd = nltk.FreqDist(word.lower() for (word, tag) in tagged_text if tag in taglist)

    for word, count in word_fd.iteritems():
        if word in word_list:
            word_list_dict[word+'_relative_frequency'] = float(count)/length_tagged_text

    # create list of results in order to preserve function word list ordering
    # ordered_func_word_distributions = [word_list_dict[word] for word in word_list]

    return word_list_dict


def create_csv(author_name, book_title, file_name):
    output_dir = constants.FINGERPRINTS_PATH

    # create output file in output folder, with name of input folder
    try:
        os.makedirs(output_dir + author_name + '/' + book_title)
    except:
        pass

    file_number = file_name.split('.')[0]
    output_file = open(output_dir + author_name + '/' + book_title + '/' + file_number + '.csv', 'w')

    # create csv writer object and write the fieldnames to first row
    csv_writer = csv.writer(output_file, delimiter='\t')
    csv_writer.writerow(['target'] + constants.CHUNK_MODEL_FINGERPRINT_FIELDS)
    return csv_writer

def compute_all_fingerprints(root_path=constants.CHUNKS_PATH):
    to_fingerprint = []
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':  # prevent hidden files e.g .DS_Store
                author = dir_name.split('/')[-2]
                title = dir_name.split('/')[-1]
                chunk_path = dir_name+'/'+file
                to_fingerprint.append((author, title, file, chunk_path))

    fingerprints = []
    if (constants.PARALLEL):
        #TODO: Broken fix to use new arguments
        import celery
        import tasks
        group = celery.group((tasks.compute_fingerprint.s(author, title, file) for (author, title, file) in to_fingerprint))
        result = group()
        fingerprints = result.get()
    else:
        for (author, title, file, chunk_path) in to_fingerprint:
            fingerprints.append(fingerprint_text(author, title, file, chunk_as_path=chunk_path))
    return fingerprints

if __name__ == '__main__':
    author = 'hemingway'
    title = 'completeshortstories'
    chunk_name = '0000.txt'
    print fingerprint_text(author, title, chunk_name, write_to_csv=True,
                                  chunk_as_path='data/chunks/hemingway/completeshortstories/0000.txt')
