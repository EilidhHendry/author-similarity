import constants
from util import generate_directory_name, tokenize_sentences

import string
import os
import nltk


def generate_text_path(author, title):
    output_directory = constants.PLAINTEXT_PATH + generate_directory_name(author) + "/" + generate_directory_name(title) + ".txt"
    return output_directory

def chunk_text(input_path):

    with open(input_path) as in_file:
        input_chunk = in_file.read()

        # tokenise into sentences
        sentences = tokenize_sentences(input_chunk)

        current_chunk = []
        current_chunk_word_count = 0
        for sentence in sentences:
            # TODO: Don't just remove non-ascii
            # add the sentence to the current chunk and remove non-ascii characters
            current_chunk = current_chunk + sentence

            for word in sentence:

                # increment the word count if not whitespace
                if word not in string.whitespace:
                    current_chunk_word_count += 1

                if current_chunk_word_count == constants.CHUNK_SIZE:

                    # first join some punctuation to the previous word (returns generator object)
                    punctuation_joined_chunk = join_punctuation(current_chunk)

                    # then convert list of words to string
                    chunk = ' '.join(punctuation_joined_chunk)

                    yield chunk

                    # start over for the next chunk
                    current_chunk = []
                    current_chunk_word_count = 0

        final_chunk = ' '.join(current_chunk)
        yield final_chunk

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


def chunk_dir(root_path=constants.PREPROCESSED_PATH):
    # dir_name: the current dir looking in
    # sub_dirs: list of sub-directories in the current directory.
    # files: list of files in the current directory.
    to_chunk = []
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':  # prevent hidden files e.g .DS_Store
                path = os.path.join(dir_name, file)
                to_chunk.append(path)

    for current_file_path in to_chunk:
        chunk_text(current_file_path)

if __name__ == '__main__':
    chunk_dir(constants.PREPROCESSED_PATH)
