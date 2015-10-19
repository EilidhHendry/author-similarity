import string
import os

def preprocess(author_name, book_title, input_filename):
    with open(input_filename) as input_text:
        split_texts = split_text(input_text, book_title)




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


if __name__== '__main__':
    with open('README.md') as input_file:
        print split_text(input_file, 'README', chunk_size=10)