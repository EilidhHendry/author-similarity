import string
import nltk
import csv

def preprocess(author_name, book_title, input_dir):

    # create csv writer object, output file and write headers to file
    csv_writer = create_csv(book_title)

    corpus = nltk.corpus.reader.PlaintextCorpusReader(input_dir, r'.*\.txt$')

    for text_name in corpus.fileids():

        # progress update
        print text_name

        # get avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation
        simple_stats = analyze_text(corpus, text_name)

        # tag current text
        # requires nltk maxent_treebank_tagger downloaded
        pos_current_text = nltk.pos_tag(corpus.words(fileids=text_name))

        # get normalised function word distributions
        function_word_distribution = get_function_word_distribution(pos_current_text, corpus, text_name)

        # get normalised pos distributions
        pos_distribution = get_pos_counts(pos_current_text, corpus, text_name)

        # write current text to csv file
        csv_writer.writerow([author_name]+simple_stats+function_word_distribution+pos_distribution)


def split_text(input_file, book_title, chunk_size=10000):
    current_chunk = []
    current_chunk_word_count = 0
    file_count = 0

    for line in input_file:
        words = line.split()

        for word in words:
            # preserve spaces without affecting word count
            current_chunk.append(word)

            if word not in string.whitespace:
                current_chunk_word_count += 1

            if current_chunk_word_count == chunk_size:
                chunk = ' '.join(current_chunk)
                # create new file with 0 padding
                output_file = open(book_title+"{0:02d}.txt".format(file_count),'w')
                file_count+=1
                # print the current chunk to file
                print>>output_file, chunk
                # start over for the next chunk
                current_chunk = []
                current_chunk_word_count = 0

    # print the remaining text to a new file
    final_chunk = ' '.join(current_chunk)
    output_file = open(book_title+"{0:02d}.txt".format(file_count),'w')
    print>>output_file, final_chunk


def analyze_text(corpus, filename):
        chars = corpus.raw(fileids=[filename])
        words = corpus.words(fileids=[filename])
        sentences = corpus.sents(fileids=[filename])
        word_count = len(words)
        char_count = len(chars)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in corpus.words(fileids=[filename])))
        punctuation_count = count_punctuation(corpus.raw(fileids=[filename]))
        avg_word_length = float(char_count)/word_count
        avg_sentence_length = float(word_count)/sentence_count
        lexical_diversity = float(vocab_count) / word_count
        percentage_punctuation = float(punctuation_count) / char_count
        return [avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation]


def count_punctuation(raw_corpus):
    punctuation_marks = ['!',',','.',':','"','?','-',';','(',')','[',']','\\','/']
    punc = [char for char in raw_corpus if char in punctuation_marks]
    return len(punc)


def get_pos_counts(tagged_text, corpus, filename):
    # TODO: check should be normalised by no. words or no. tags
    tag_list = ['PRP$', 'VBG', 'VBD', 'VBN', 'POS', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', 'NN', 'FW', 'TO',
                 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX',
                 'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'UH']
    # initialise dictionary with tag list as keys
    final_pos_distribution = {key: 0 for key in tag_list}

    # create frequency distribution of tags in text
    tagged_text_freq_dist = nltk.FreqDist(tag for (word, tag) in tagged_text)

    # find the length of the current text
    text_length = len(corpus.words(fileids=filename))

    # loop through the frequency distribution dictionary, normalise and add to empty but initialised dictionary of tags
    # this approach preserves 0 values for tags which do not occur in current text
    for tag, count in tagged_text_freq_dist.iteritems():
        final_pos_distribution[tag] = float(count)/text_length

    # create list of results in order to preserve tag list ordering
    ordered_pos_distributions = [final_pos_distribution[tag] for tag in tag_list]
    return ordered_pos_distributions


def get_function_word_distribution(tagged_text, plain_corpus, text_name):
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

    text_length = len(plain_corpus.words(fileids=text_name))

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
    output_file = open('temp/fingerprint_output/'+book_title+'.csv', 'w')

    # create csv writer object and write the fieldnames to first row
    csv_writer = csv.writer(output_file, delimiter='\t')
    csv_writer.writerow(fieldnames)
    return csv_writer

if __name__ == '__main__':

    preprocess('hemingway', 'acrosstheriverandintothetrees', 'test_data/acrosstheriverandintothetrees')