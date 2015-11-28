__author__ = 'eilidhhendry'

import os

def combine_chunks(root_path):
    output_path = 'data/combined_fingerprint/'
    output_file = open(output_path +'combined_fingerprints.csv', 'w')
    first_iteration = True

    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith('.csv'):
                current_file_path = os.path.join(dir_name, file)
                with open(current_file_path) as file_content:
                    for line in file_content:
                        if first_iteration:
                            print >> output_file, line.strip()
                            first_iteration = False
                        words = line.split('\t')
                        if words[0] != 'target':
                            print >> output_file, line.strip()


if __name__ == '__main__':
    root_path = 'data/fingerprint_output'
    output_path = 'data/fingerprint_output/'
    combine_chunks(root_path)