import constants

def generate_directory_name(name):
    directory_name = "".join([char.lower() for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name

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
