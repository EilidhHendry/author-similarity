import collections

from similarity.classifier import compute_fingerprint

test_file = 'syllable_test_data.txt'


def parse_test_file(input_file):
    syllable_dict = collections.defaultdict(list)

    with open(input_file) as file_content:
        for line in file_content:
            word, num_syllables_str = line.strip().split('==')
            num_syllables = int(num_syllables_str)
            syllable_dict[num_syllables].append(word)

    return syllable_dict


def run_test():
    results_dict = collections.Counter()
    incorrect_dict = collections.defaultdict(list)
    lengths = []
    syllable_dict = parse_test_file(test_file)

    for actual_num_syllables, word_list in syllable_dict.items():
        lengths.append(len(word_list))
        for word in word_list:
            predicted_num_syllables = compute_fingerprint.number_syllables(word)
            if predicted_num_syllables == actual_num_syllables:
                results_dict[actual_num_syllables] += 1
            else:
                incorrect_dict[actual_num_syllables].append((word, predicted_num_syllables))

    for actual_num_syllables in syllable_dict.keys():
        correct = results_dict[actual_num_syllables]
        incorrect_list = incorrect_dict[actual_num_syllables]
        total_num_words = len(incorrect_list) + correct

        print actual_num_syllables, ':', correct, ' / ', total_num_words, ' == ', (float(
            correct) * 100) / total_num_words, '%'
        print 'incorrect values: ', incorrect_list


if __name__ == '__main__':
    run_test()
