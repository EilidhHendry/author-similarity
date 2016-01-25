import constants
import string
import os
import nltk

def generate_directory_name(name):
    directory_name = "".join([char.lower() for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name


def generate_chunk_path(author, title):
    output_directory = constants.CHUNKS_PATH + generate_directory_name(author) + "/" + generate_directory_name(title) + "/"
    return output_directory


def generate_text_path(author, title):
    output_directory = constants.PLAINTEXT_PATH + generate_directory_name(author) + "/" + generate_directory_name(title) + ".txt"
    return output_directory


def chunk_text(input_path, author, title):
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
        # TODO: Don't just remove non-ascii
        # add the sentence to the current chunk and remove non-ascii characters
        current_chunk = current_chunk + [word.encode('ascii', 'ignore') for word in sentence]

        for word in sentence:

            # increment the word count if not whitespace
            if word not in string.whitespace:
                current_chunk_word_count += 1

            if current_chunk_word_count == constants.CHUNK_SIZE:

                # first join some punctuation to the previous word (returns generator object)
                punctuation_joined_chunk = join_punctuation(current_chunk)

                # then convert list of words to string
                chunk = ' '.join(punctuation_joined_chunk)

                # create new file in the output directory with 0 padding
                output_file = open(chunk_output_directory+"{0:04d}.txt".format(file_count),'w')
                file_count+=1

                # print the current chunk to file
                print>>output_file, chunk

                # start over for the next chunk
                current_chunk = []
                current_chunk_word_count = 0

    # print the remaining text to a new file
    final_chunk = ' '.join(current_chunk)
    output_file = open(chunk_output_directory+"{0:04d}.txt".format(file_count),'w')
    print>>output_file, final_chunk


def join_punctuation(word_list):
    # note only includes the punctuation marks you want to join to prev word
    punctuation_marks = ['!', ',', '.', ':', '"', '\'', '?', ';']
    iter_word_list = iter(word_list)
    current_word = next(iter_word_list)

    for next_word in iter_word_list:
        if next_word in punctuation_marks:
            current_word += next_word
        else:
            yield current_word
            current_word = next_word
    yield current_word


def chunk_dir(root_path):
    # dir_name: the current dir looking in
    # sub_dirs: list of sub-directories in the current directory.
    # files: list of files in the current directory.
    to_chunk = []
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':
                author = dir_name.split('/')[-2]
                title = file.split('.')[0]
                path = os.path.join(dir_name, file)
                to_chunk.append((path, author, title))

    if (constants.PARALLEL):
        import celery
        import tasks
        group = celery.group((tasks.chunk_text.s(current_file_path, author, title) for (current_file_path, author, title) in to_chunk))
        result = group()
        result.get()
    else:
        for (current_file_path, author, title) in to_chunk:
            chunk_text(current_file_path, author, title)

if __name__ == '__main__':
    chunk_dir(constants.PREPROCESSED_PATH)
