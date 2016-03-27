import constants
from util import tokenize_sentences

import string
import codecs

def chunk_text(input_path):

    with codecs.open(input_path, encoding="utf-8") as in_file:
        input_file = in_file.read()

        # tokenise into sentences
        sentences = tokenize_sentences(input_file)

        current_chunk = []
        current_chunk_word_count = 0
        for sentence in sentences:
            # TODO: Don't just remove non-ascii
            # add the sentence to the current chunk and remove non-ascii characters
            current_chunk.append(sentence)

            for word in sentence:

                # increment the word count if not whitespace
                if word not in string.whitespace:
                    current_chunk_word_count += 1

                if current_chunk_word_count == constants.CHUNK_SIZE:

                    yield current_chunk

                    # start over for the next chunk
                    current_chunk = []
                    current_chunk_word_count = 0

        yield current_chunk
