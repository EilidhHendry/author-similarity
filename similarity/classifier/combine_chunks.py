__author__ = 'eilidhhendry'

import os
import constants

def combine_chunks(root_path):
    output_file = open(constants.COMBINED_FINGERPRINT_FILE_PATH, 'w')
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
    fingerprint_path = constants.FINGERPRINTS_PATH
    combine_chunks(fingerprint_path)