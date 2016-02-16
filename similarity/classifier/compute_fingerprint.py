import constants
import os
import nltk
import csv
import timeit
import string



pronounciation_dict = nltk.corpus.cmudict.dict()
punctuation_marks = ['!', ',', '.', ':', '"', '\'', '?', '-', ';', '(', ')', '[', ']', '\\', '/', '`']


def fingerprint_text(author_name, book_title, chunk_name, write_to_csv=True):

    # get the directory name and text name from file path
    text_path = constants.CHUNKS_PATH + author_name + "/" + book_title

    # create an nltk corpus from the current chunk
    corpus = nltk.corpus.reader.PlaintextCorpusReader(text_path, chunk_name)

    # find the length of the current chunk to be used for normalisation
    text_length = len(corpus.words())

    # list to return calculated fingerprints, begins with author_name for target
    results = [author_name]

    # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
    # store results in dictionary
    avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation = analyze_text(corpus)
    analyze_text_results = {
    'avg_word_length' : avg_word_length,
    'avg_sentence_length' : avg_sentence_length,
    'lexical_diversity' : lexical_diversity,
    'percentage_punctuation' : percentage_punctuation
    }

    for field_name in ['avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation']:
        if field_name in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
            results.append(analyze_text_results[field_name])

    if 'avg_word_length_syllables' in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
        # get avg num syllables per word
        avg_syllables_result  = avg_syllables(corpus.words())
        results.append(avg_syllables_result)

    # find the function words in the list of fields
    function_word_list = get_function_word_list(constants.CHUNK_MODEL_FINGERPRINT_FIELDS)
    #find the pos tags in the list of fields
    tag_list = get_tag_list(constants.CHUNK_MODEL_FINGERPRINT_FIELDS)

    # only tag the text if finding function words or pos tags
    if function_word_list or tag_list:
        # tag current text
        # requires nltk maxent_treebank_tagger downloaded
        pos_current_text = nltk.pos_tag(corpus.words())

        # get normalised function word distributions
        function_word_distribution = get_function_word_distribution(pos_current_text, text_length, function_word_list)
        results.extend(function_word_distribution)

        # get normalised pos distributions
        pos_distribution = get_pos_counts(pos_current_text, text_length, tag_list)
        results.extend(pos_distribution)

    if write_to_csv:
        fingerprint_to_csv(results, author_name, book_title, chunk_name)

    return results

def fingerprint_text_string(author_name, book_title, chunk_name, write_to_csv=True):

    # get the directory name and text name from file path
    text_path = constants.CHUNKS_PATH + author_name + "/" + book_title + '/' + chunk_name

    text_content = open(text_path).read()

    words = tokenize_words(text_content)

    # find the length of the current chunk to be used for normalisation
    text_length = len(words)

    # list to return calculated fingerprints, begins with author_name for target
    results = [author_name]

    # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
    # store results in dictionary
    avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation = analyze_text_string(text_content)
    analyze_text_results = {
    'avg_word_length' : avg_word_length,
    'avg_sentence_length' : avg_sentence_length,
    'lexical_diversity' : lexical_diversity,
    'percentage_punctuation' : percentage_punctuation
    }

    for field_name in ['avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation']:
        if field_name in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
            results.append(analyze_text_results[field_name])

    if 'avg_word_length_syllables' in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
        # get avg num syllables per word
        avg_syllables_result  = avg_syllables(words)
        results.append(avg_syllables_result)

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
        function_word_distribution = get_function_word_distribution(pos_current_text, text_length, function_word_list)
        results.extend(function_word_distribution)

        # get normalised pos distributions
        pos_distribution = get_pos_counts(pos_current_text, text_length, tag_list)
        results.extend(pos_distribution)

    if write_to_csv:
        fingerprint_to_csv(results, author_name, book_title, chunk_name)

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


def fingerprint_to_csv(fingerprint_list, author_name, book_title, chunk_name):
    # create csv writer object, output file and write headers to file
    csv_writer = create_csv(author_name, book_title, chunk_name)

    # write current text to csv file
    csv_writer.writerow(fingerprint_list)


def analyze_text(input_chunk):
        chars = input_chunk.raw()
        words = input_chunk.words()
        sentences = input_chunk.sents()
        word_count = len(words)
        char_count = len(chars)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in words))
        avg_word_length = float(char_count)/word_count
        avg_sentence_length = float(word_count)/sentence_count
        lexical_diversity = float(vocab_count) / word_count
        punctuation_count = len([char for char in chars if set(char).intersection(set(punctuation_marks))])
        percentage_punctuation = float(punctuation_count) / char_count
        return avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation

def analyze_text_string(input_chunk):
        chars = input_chunk.replace(" ","")
        words = tokenize_words(input_chunk.translate(None, string.punctuation))
        sentences = tokenize_sentences(input_chunk)
        word_count = len(words)
        char_count = len(chars)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in words))
        if word_count > 0:
            avg_word_length = float(char_count)/word_count
            lexical_diversity = float(vocab_count) / word_count
        else:
            avg_word_length = 0
            lexical_diversity = 0
        if sentence_count > 0:
            avg_sentence_length = float(word_count)/sentence_count
        else:
            avg_sentence_length = 0
        punctuation_count = len([char for char in chars if set(char).intersection(set(punctuation_marks))])
        if char_count > 0:
            percentage_punctuation = float(punctuation_count) / char_count
        else:
            percentage_punctuation = 0
        return avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation

def number_syllables(word):
    if word in pronounciation_dict:
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
            tag_list.append(tag)
    return tag_list


def get_pos_counts(tagged_text, text_length, tag_list):
    # TODO: check should be normalised by no. words or no. tags

    # initialise dictionary with tag list as keys
    final_pos_distribution = {key: 0 for key in tag_list}

    # create frequency distribution of tags in text
    tagged_text_freq_dist = nltk.FreqDist(tag for (word, tag) in tagged_text)

    # loop through the frequency distribution dictionary, normalise and add to empty but initialised dictionary of tags
    # this approach preserves 0 values for tags which do not occur in current text
    for tag, count in tagged_text_freq_dist.iteritems():
        final_pos_distribution[tag] = float(count)/text_length

    # create list of results in order to preserve tag list ordering
    ordered_pos_distributions = [final_pos_distribution[tag] for tag in tag_list]
    return ordered_pos_distributions


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


def get_function_word_distribution(tagged_text, text_length, word_list):
    # TODO: check normalised by no. words or no. tags
    taglist = 'PRP PRP$ WP WP$ CC MD UH RP IN TO WDT DT PDT'.split()

    word_fd = nltk.FreqDist(word.lower() for (word, tag) in tagged_text if tag in taglist)

    # initialise dictionary with word list as keys
    word_list_dict = {key: 0 for key in word_list}

    for word, count in word_fd.iteritems():
        if word in word_list:
            word_list_dict[word] = float(count)/text_length

    # create list of results in order to preserve function word list ordering
    ordered_func_word_distributions = [word_list_dict[word] for word in word_list]

    return ordered_func_word_distributions


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
                to_fingerprint.append((author, title, file))

    fingerprints = []
    if (constants.PARALLEL):
        import celery
        import tasks
        group = celery.group((tasks.compute_fingerprint.s(author, title, file) for (author, title, file) in to_fingerprint))
        result = group()
        fingerprints = result.get()
    else:
        for (author, title, file) in to_fingerprint:
            fingerprints.append(fingerprint_text(author, title, file))
    return fingerprints

if __name__ == '__main__':
    author = 'hemingway'
    title = 'completeshortstories'
    chunk_name = '0000.txt'
    setup_command = "from compute_fingerprint import fingerprint_text, fingerprint_text_string"
    print timeit.timeit(setup=setup_command, stmt='fingerprint_text(\'hemingway\',  \'completeshortstories\', \'0000.txt\',  write_to_csv=False)', number=1)
    print timeit.timeit(setup=setup_command, stmt='fingerprint_text_string(\'hemingway\',  \'completeshortstories\', \'0000.txt\',  write_to_csv=False)', number=1)
