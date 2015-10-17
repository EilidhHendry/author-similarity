__author__ = 'eilidhhendry'

import csv
import os
import ast

import nltk


class ComputeFingerprint:

    def __init__(self):
        fieldnames = ['target', 'avg_word_length', 'avg_sentence_length', 'lexical_diversity', 'percentage_punctuation',
                      'the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                      'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                      'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                      'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                      'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                      'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                      'another', 'myself' 'PRP$', 'VBG', 'VBD', 'VBN',
                      'POS', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', 'NN', 'FW', 'TO', 'PRP', 'RB', 'NNS', 'NNP',
                      'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX', 'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'UH']
        self.main('/Users/eilidhhendry/PycharmProjects/author-similarity/test_data/plain_test/hemingway_imitation', '/Users/eilidhhendry/PycharmProjects/author-similarity/test_data/tagged_test/hemingway_imitation', fieldnames)

    def main(self, plain_dir, tagged_dir, fieldnames):

        # take input dir and create nltk Corpus from .txt files, split into categories by author name (folder name)
        corpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader(plain_dir, r'.*\.txt$', cat_pattern=r'(\w+)/*')

        # take tagged dir and create tagged nltk Corpus
        tagged_corpus = nltk.corpus.reader.CategorizedPlaintextCorpusReader(tagged_dir, r'.*\.txt$', cat_pattern=r'(\w+)/*')

        # try to create the output directory
        try:
            os.mkdir('temp/fingerprint_output')
        except OSError:
            # already exists so skip
            pass

        # create output file in output folder, with name of input folder
        output_file = open('temp/fingerprint_output/hemingway_imitation.csv', 'w')

        # create csv writer object and write the fieldnames to first row
        csv_writer = csv.writer(output_file, delimiter='\t')
        csv_writer.writerow(fieldnames)

        # loop through all the categories (authors)
        for category in corpus.categories():

            # loop through all the files (texts) in the current category (authors)
            for text_name in corpus.fileids(category):

                # print author name (filename) to terminal
                print text_name

                # create list for the current row/author in the csv file
                row = []

                # store the author's name as the first item
                row.append(category)

                # get the basic stats for this text and add to list
                stats = self.analyze_text(corpus, text_name)
                row = row + stats

                """
                # get the average number of syllables and add to list
                avg_syllables = self.avg_num_syllables(corpus, text_name)
                row.append(avg_syllables)

                # get the readability scores for this text and add to list
                readability_dict = self.readabilities(corpus, text_name)
                for key, value in readability_dict.items():
                    row.append(value)
                """

                # get the function word distrubution and add to list
                function_counts = self.function_words(text_name)
                row = row + function_counts

                # get the pos counts and add to list
                pos_counts = self.get_pos_counts(tagged_corpus, corpus, text_name)
                row = row + pos_counts

                # write the current row to file
                csv_writer.writerow(row)

    def analyze_text(self, corpus, filename):
        chars = corpus.raw(fileids=[filename])
        words = corpus.words(fileids=[filename])
        sentences = corpus.sents(fileids=[filename])
        word_count = len(words)
        char_count = len(chars)
        sentence_count = len(sentences)
        vocab_count = len(set(w.lower() for w in corpus.words(fileids=[filename])))
        punctuation_count = self.count_punc(corpus.raw(fileids=[filename]))
        avg_word_length = float(char_count)/word_count
        avg_sentence_length = float(word_count)/sentence_count
        lexical_diversity = float(vocab_count) / word_count
        percentage_punctuation = float(punctuation_count) / char_count
        return [avg_word_length, avg_sentence_length, lexical_diversity, percentage_punctuation]

    @staticmethod
    def count_punc(raw_corpus):
        punctuation_marks = ['!',',','.',':','"','?','-',';','(',')','[',']','\\','/']
        punc = [char for char in raw_corpus if char in punctuation_marks]
        return len(punc)

    def readabilities(self, corpus, filename):
        rd = readability.Readability(corpus.raw(fileids=[filename]))
        readability_dict = {
        'ARI': rd.ARI(),
        'flesch_reading_ease': rd.FleschReadingEase(),
        'flesch_kincaid_grade_level': rd.FleschKincaidGradeLevel(),
        'gunning_fog_index': rd.GunningFogIndex(),
        'SMOG_Index': rd.SMOGIndex(),
        'coleman_liau_index': rd.ColemanLiauIndex(),
        'LIX': rd.LIX(),
        'RIX': rd.RIX()}
        return readability_dict

    def avg_num_syllables(self, corpus, filename):
        syllable_count = utils.count_syllables(corpus.words(fileids=filename))
        num_words = len(corpus.words(fileids=filename))
        return float(syllable_count)/num_words

    def get_pos_counts(self, tagged_corpus, corpus, filename):
        pos_corpus = tagged_corpus.raw(fileids=filename)
        tuple_corpus = ast.literal_eval(pos_corpus)
        pos_corpus_fd = nltk.FreqDist(tag for (word, tag) in tuple_corpus)
        normalised = {}
        length = len(corpus.words(fileids=filename))
        for tag, count in pos_corpus_fd.iteritems():
            normalised[tag] = float(count)/length
        pos_list = ['PRP$', 'VBG', 'VBD', 'VBN', 'POS', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', 'NN', 'FW', 'TO',
                     'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX',
                     'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'UH']
        result = []
        for tag in pos_list:
            if tag in normalised:
                result.append(normalised[tag])
            else:
                result.append(0)
        return result

    def function_words(self, input_filename):
        word_list = ['the', 'and', 'of', 'a', 'to', 'in', 'i', 'he', 'it', 'that', 'you', 'his', 'with', 'on', 'for', 'at',
                     'as', 'but', 'her', 'they', 'she', 'him', 'all', 'this', 'we', 'from', 'or', 'out', 'an', 'my', 'by',
                     'up', 'what', 'me', 'no', 'like', 'would', 'if', 'about', 'which', 'them', 'into', 'who', 'could',
                     'can', 'some', 'their', 'over', 'down', 'your', 'will', 'its', 'any', 'through', 'after', 'off', 'than',
                     'our', 'us', 'around', 'these', 'because', 'must', 'before', 'those', '&', 'should', 'himself', 'both',
                     'against', 'may', 'might', 'shall', 'since', 'de', 'within', 'between', 'each', 'under', 'until', 'toward',
                     'another', 'myself']

        file_dict = {}

        with open('temp/function_word_counts/function_test_counts.txt') as infile:
            for line in infile:
                filename, tuple_list = line.split('\t')
                if filename.strip() == input_filename:
                    tuple_line = ast.literal_eval(tuple_list)
                    for word, count in tuple_line:
                        if word in word_list:
                            file_dict[word] = count
        result = []
        for word in word_list:
            if word in file_dict:
                result.append(file_dict[word])
            else:
                result.append(0)

        return result

if __name__ == '__main__':
    results = ComputeFingerprint()

