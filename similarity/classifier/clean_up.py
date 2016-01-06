 # -*- coding: utf-8 -*-
__author__ = 'eilidhhendry'
import constants
import os

def generate_directory_name(name):
    directory_name = "".join([char for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name

def generate_preprocessed_path(author, title):
    output_directory = constants.PREPROCESSED_PATH + generate_directory_name(author) + "/" + generate_directory_name(title) + "/"
    return output_directory

def clean_unicode(input_string):
    clean_string = input_string.strip().replace("—", "-").replace('“', '"').replace('”', '"').replace("’", "'")\
                    .replace("é", "e").replace("í", 'i').replace("ó", "o").replace("…","...")
    return clean_string

def clean_file(input_path, author, title):
    preprocessed_output_directory = generate_preprocessed_path(author, title)

    try:
        os.makedirs(preprocessed_output_directory)
    except:
        pass

    text_name = os.path.basename(input_path)
    output_file = open(preprocessed_output_directory+'/'+text_name, 'w')

    with open(input_path) as file_content:
        for line in file_content:
            clean_line = clean_unicode(line)
            print >> output_file, clean_line

def clean_directories(root_path):
    to_preprocess = []
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':
                author = dir_name.split('/')[-1]
                title = file.split('.')[0]
                path = os.path.join(dir_name, file)
                to_preprocess.append((path, author, title))

    if (constants.PARALLEL):
        import celery
        import tasks
        group = celery.group((tasks.clean_text.s(current_file_path, author, title) for (current_file_path, author, title) in to_preprocess))
        result = group()
        result.get()
    else:
        for (current_file_path, author, title) in to_preprocess:
            clean_file(current_file_path, author, title)