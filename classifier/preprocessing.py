import string
import os
import nltk


def split_text_sentences(input_file, book_title, chunk_size=10000):

     # get the directory name and text name from file path
    text_path = os.path.dirname(input_file)
    text_name = os.path.basename(input_file)

    corpus = nltk.corpus.reader.PlaintextCorpusReader(text_path, text_name)

    print len(corpus.words())

    sentences = corpus.sents()

    current_chunk = []
    current_chunk_word_count = 0
    file_count = 0
    for sentence in sentences:

        new_sentence = []
        for word in sentence:
            new_sentence.append(word.encode('ascii', 'ignore'))

        current_chunk = current_chunk + new_sentence
        for word in new_sentence:
            if word not in string.whitespace:
                current_chunk_word_count += 1

            if current_chunk_word_count == chunk_size:
                chunk = ' '.join(current_chunk)
                # create new file with 0 padding
                output_file = open('test/acrosstheriverandintothetrees/'+book_title+"{0:02d}.txt".format(file_count),'w')
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

def word_count(input_file):
    word_counts = 0
    with open(input_file) as file_content:
        for line in file_content:
            words = line.split()
            for word in words:
                if word not in string.whitespace:
                    word_counts +=1
    print word_counts

if __name__ == '__main__':
    try:
        os.mkdir('test/acrosstheriverandintothetrees')
    except:
        pass

    split_text_sentences('test/acrosstheriverandintothetrees.txt', 'acrosstheriverandintothetrees', chunk_size=10000)

    for subdir, dirs, files in os.walk('test/acrosstheriverandintothetrees/'):
        for file in files:
            word_count('test/acrosstheriverandintothetrees/'+file)

    print '--------------'

    for subdir, dirs, files in os.walk('test_data/acrosstheriverandintothetrees/'):
        for file in files:
            word_count('test_data/acrosstheriverandintothetrees/' + file)