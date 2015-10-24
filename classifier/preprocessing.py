import string
import os
import nltk


def split_text(input_path, output_path, book_title, chunk_size=10000):

    output_directory = output_path+'/'+book_title
    try:
        os.mkdir(output_directory)
    except:
        pass

     # get the directory name and text name from file path
    text_path = os.path.dirname(input_path)
    text_name = os.path.basename(input_path)

    # create an nltk corpus from the input file
    corpus = nltk.corpus.reader.PlaintextCorpusReader(text_path, text_name)

    # tokenise into sentences
    sentences = corpus.sents()

    current_chunk = []
    current_chunk_word_count = 0
    file_count = 0
    for sentence in sentences:
        # add the sentence to the current chunk and remove non-ascii characters
        current_chunk = current_chunk + [word.encode('ascii', 'ignore') for word in sentence]
        for word in sentence:

            # increment the word count if not whitespace
            if word not in string.whitespace:
                current_chunk_word_count += 1

            if current_chunk_word_count == chunk_size:

                # convert list of words to string
                chunk = ' '.join(current_chunk)

                # create new file in the output directory with 0 padding
                output_file = open(output_directory+'/'+book_title+"{0:02d}.txt".format(file_count),'w')
                file_count+=1

                # print the current chunk to file
                print>>output_file, chunk

                # start over for the next chunk
                current_chunk = []
                current_chunk_word_count = 0

    # print the remaining text to a new file
    final_chunk = ' '.join(current_chunk)
    output_file = open(output_directory+'/'+book_title+"{0:02d}.txt".format(file_count),'w')
    print>>output_file, final_chunk

# for testing
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

    split_text('test/acrosstheriverandintothetrees.txt', 'test/', 'acrosstheriverandintothetrees', chunk_size=10000)

