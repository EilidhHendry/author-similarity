import constants
import string
import os
import nltk

def generate_directory_name(name):
    directory_name = "".join([char for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name

def generate_chunk_path(author, title):
    output_directory = constants.CHUNKS_PATH + "/" + generate_directory_name(author) + "/" + generate_directory_name(title) + "/"
    return output_directory

def generate_text_path(author, title):
    output_directory = constants.PLAINTEXT_PATH + "/" + generate_directory_name(author) + "/" + generate_directory_name(title) + ".txt"
    return output_directory

def chunk_text(input_path, author, title, chunk_size=10000):
    chunk_output_directory = generate_chunk_path(author, title)

    try:
        os.makedirs(chunk_output_directory)
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
                output_file = open(chunk_output_directory+"{0:02d}.txt".format(file_count),'w')
                file_count+=1

                # print the current chunk to file
                print>>output_file, chunk

                # start over for the next chunk
                current_chunk = []
                current_chunk_word_count = 0

    # print the remaining text to a new file
    final_chunk = ' '.join(current_chunk)
    output_file = open(chunk_output_directory+"{0:02d}.txt".format(file_count),'w')
    print>>output_file, final_chunk

if __name__ == '__main__':
    author = 'hemingway'
    title = 'across the river and into the trees'
    text_output_path = generate_text_path(author, title)
    chunk_text('temp/acrosstheriverandintothetrees.txt', author, title, chunk_size=10000)
