import constants
import os
import nltk
import csv

def compute_fingerprint(author_name, book_title, chunk_name, write_to_csv=True):

    root_dir = constants.CHUNKS_PATH

    # get the directory name and text name from file path
    text_path = root_dir + author_name + "/" + book_title + "/"

    # create an nltk corpus from the current chunk
    corpus = nltk.corpus.reader.PlaintextCorpusReader(text_path, chunk_name)

    # find the length of the current chunk to be used for normalisation
    text_length = len(corpus.words())

    # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
    simple_stats = analyze_text(corpus)

    # tag current text
    # requires nltk maxent_treebank_tagger downloaded
    pos_current_text = nltk.pos_tag(corpus.words())

    # get normalised function word distributions
    function_word_distribution = get_function_word_distribution(pos_current_text, text_length)

    # get normalised pos distributions
    pos_distribution = get_pos_counts(pos_current_text, text_length)

    fingerprint_list = [author_name]+simple_stats+function_word_distribution+pos_distribution

    if write_to_csv:
        fingerprint_to_csv(fingerprint_list, author_name, book_title, chunk_name)

    return fingerprint_list


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
        punctuation_count = count_punctuation(chars)
        avg_word_length = float(char_count)/word_count
        avg_sentence_length = float(word_count)/sentence_count
        lexical_diversity = float(vocab_count) / word_count
        percentage_punctuation = float(punctuation_count) / char_count
        return [avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation]


def count_punctuation(chars):
    punctuation_marks = ['!', ',', '.', ':', '"', '\'', '?', '-', ';', '(', ')', '[', ']', '\\', '/']
    punc = [char for char in chars if char in punctuation_marks]
    return len(punc)


def get_pos_counts(tagged_text, text_length):
    # TODO: check should be normalised by no. words or no. tags
    tag_list = ['PRP$', 'VBG', 'VBD', 'VBN', 'POS', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', 'NN', 'FW', 'TO',
                 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX',
                 'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'UH']
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


def get_function_word_distribution(tagged_text, text_length):
    # TODO: check normalised by no. words or no. tags
    taglist = 'PRP PRP$ WP WP$ CC MD UH RP IN TO WDT DT PDT'.split()

    word_fd = nltk.FreqDist(word.lower() for (word, tag) in tagged_text if tag in taglist)

    word_list = ['the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                 'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                 'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                 'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                 'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                 'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                 'another', 'myself']

    # initialise dictionary with word list as keys
    word_list_dict = {key: 0 for key in word_list}

    for word, count in word_fd.iteritems():
        if word in word_list:
            word_list_dict[word] = float(count)/text_length

    # create list of results in order to preserve function word list ordering
    ordered_func_word_distributions = [word_list_dict[word] for word in word_list]

    return ordered_func_word_distributions


def create_csv(author_name, book_title, file_name):
    fieldnames = ['target', 'avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation',
                  'the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                  'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                  'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                  'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                  'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                  'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                  'another', 'myself', 'PRP$', 'VBG', 'VBD', 'VBN', 'POS', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP',
                  'NN', 'FW', 'TO', 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX',
                  'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'UH']

    output_dir = constants.FINGERPRINTS_PATH

    # create output file in output folder, with name of input folder
    try:
        os.makedirs(output_dir+author_name+'/'+book_title)
    except:
        pass

    file_number = file_name.split('.')[0]
    output_file = open(output_dir+author_name+'/'+book_title+'/'+file_number+'.csv', 'w')

    # create csv writer object and write the fieldnames to first row
    csv_writer = csv.writer(output_file, delimiter='\t')
    csv_writer.writerow(fieldnames)
    return csv_writer

def compute_all_fingerprints(root_path):
    to_fingerprint = []
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':
                author = dir_name.split('/')[-2]
                title = dir_name.split('/')[-1]
                to_fingerprint.append((author, title, file))

    if (constants.PARALLEL):
        import celery
        import tasks
        group = celery.group((tasks.compute_fingerprint.s(author, title, file) for (author, title, file) in to_fingerprint))
        result = group()
        result.get()
    else:
        for (author, title, file) in to_fingerprint:
            compute_fingerprint(author, title, file)

if __name__ == '__main__':
    compute_all_fingerprints(constants.CHUNKS_PATH)
