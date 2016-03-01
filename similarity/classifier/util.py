import textract
import os
import timeit
import constants

def generate_directory_name(name):
    directory_name = "".join([char.lower() for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name

def text_extract_textract(file_path):
    file_name, extension = os.path.splitext(file_path)
    if extension=='.txt':
        return file_path
    if extension=='.epub':
        try:
            text = textract.process(file_path)
            output_path = file_name+'.txt'
            output_file = open(output_path, 'w')
            output_file.write(text)
            return output_path
        # TODO: textract raises own error so none isn't returned on try failure
        except IOError:
            print 'Not supported file type'
            return None
    print 'Not supported file type'
    return None


def dictionary_to_list(fingerprint_dictionary):
    result_list = []
    for field in constants.CHUNK_MODEL_FINGERPRINT_FIELDS:
        if field in fingerprint_dictionary:
            result_list.append(fingerprint_dictionary[field])
    assert len(result_list) == len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS)
    return result_list

def list_to_dictionary(fingerprint_list):
    assert len(fingerprint_list) == len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS), \
    'list contains %r items but CHUNK_MODEL_FINGERPRINT_FIELDS contains %r' \
    % (len(fingerprint_list), len(constants.CHUNK_MODEL_FINGERPRINT_FIELDS))

    result_dictionary = {}
    for i, field in enumerate(constants.CHUNK_MODEL_FINGERPRINT_FIELDS):
        result_dictionary[field] = fingerprint_list[i]
    return result_dictionary
