import os
import nltk
import csv

def compute_fingerprint(author_name, book_title, input_chunk):

    # create csv writer object, output file and write headers to file
    csv_writer = create_csv(book_title)

    # get the directory name and text name from file path
    text_path = os.path.dirname(input_chunk)
    text_name = os.path.basename(input_chunk)

    # create an nltk corpus from the current chunk
    corpus = nltk.corpus.reader.PlaintextCorpusReader(text_path, text_name)

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

    # write current text to csv file
    csv_writer.writerow([author_name]+simple_stats+function_word_distribution+pos_distribution)


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
    punctuation_marks = ['!',',','.',':','"','?','-',';','(',')','[',']','\\','/']
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


def create_csv(book_title):
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

    # create output file in output folder, with name of input folder
    output_file = open('data/fingerprint_output/'+book_title+'.csv', 'w')

    # create csv writer object and write the fieldnames to first row
    csv_writer = csv.writer(output_file, delimiter='\t')
    csv_writer.writerow(fieldnames)
    return csv_writer

if __name__ == '__main__':

    compute_fingerprint('hemingway', 'acrosstheriverandintothetrees', 'test_data/acrosstheriverandintothetrees/acrosstheriverandintothetrees0.txt')
