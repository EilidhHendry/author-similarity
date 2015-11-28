import chunk
import compute_fingerprint
import svm
import os
import csv
import timeit
import time
import walkdir
import shutil

def create_csv():
    # create output file in output folder, with name of input folder
    output_file = open('data/chunk_eval_results/chunk_eval_results.csv', 'w')

    # create csv writer object
    csv_writer = csv.writer(output_file, delimiter='\t')

    # write the fieldnames to the first row
    fieldnames = ['chunk size', 'time to chunk', 'time to compute fingerprint', 'time to combine', 'time to train', 'total time', 'accuracy']
    csv_writer.writerow(fieldnames)
    return csv_writer

def chunk_dir(root_path, chunk_size):
    # dir_name: the current dir looking in
    # sub_dirs: list of sub-directories in the current directory.
    # files: list of files in the current directory.
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':
                author = dir_name.split('/')[-1]
                title = file.split('.')[0]
                current_file_path = os.path.join(dir_name, file)
                print current_file_path
                chunk.chunk_text(current_file_path, author, title, chunk_size=chunk_size)

def compute_all_fingerprints(root_path):
    for dir_name, sub_dirs, files in os.walk(root_path):
        for file in files:
            if file[0] != '.':
                author = dir_name.split('/')[-2]
                title = dir_name.split('/')[-1]
                print "%s - %s" % (author, title)
                compute_fingerprint.compute_fingerprint(author, title, file)

def time_chunking(root_path, chunk_size, repetitions):
    # TODO - string formatting
    chunk_command = "chunk_dir(\'" + root_path + "\', " + str(chunk_size) + ")"
    setup_command = "from __main__ import chunk_dir"
    time = timeit.repeat(stmt=chunk_command, setup=setup_command, repeat=repetitions, number=1)
    return time

def time_compute_all_fingerprints(root_path, repetitions):
    compute_fingerprint_command = "compute_all_fingerprints(\'" + root_path + "\')"
    setup_command = "from __main__ import compute_all_fingerprints"
    time = timeit.repeat(stmt=compute_fingerprint_command, setup=setup_command, repeat=repetitions, number=1)
    return time

def time_combine(fingerprints_path, repetitions):
    combine_command = "combine_chunks(\'" + fingerprints_path + "\')"
    setup_command = "from combine_chunks import combine_chunks"
    time = timeit.repeat(stmt=combine_command, setup=setup_command, repeat=repetitions, number=1)
    return time

def time_svm(input_csv, repetitions):
    svm_command = "train_csv(\'" + input_csv + "\')"
    setup_command = "from svm import train_csv"
    time = timeit.repeat(stmt=svm_command, setup=setup_command, repeat=repetitions, number=1)
    return time

def find_accuracy(fingerprint):
    clf, test_data, test_targets = svm.train_csv(fingerprint)
    accuracy = svm.svm_accuracy(clf, test_data, test_targets)
    return accuracy

def eval_chunk(chunk_size, repetitions):
    plaintext_path = 'data/texts'
    chunks_path = 'data/chunks'
    fingerprints_path = 'data/fingerprint_output'
    combined_fingerprint_path = 'data/combined_fingerprint/combined_fingerprints.csv'

    csv_writer = create_csv()

    print "chunking"
    chunk_times = time_chunking(plaintext_path, chunk_size, repetitions)
    print "fingerprinting"
    compute_fingerprint_times = time_compute_all_fingerprints(chunks_path, repetitions)
    print "combining"
    combine_times = time_combine(fingerprints_path, repetitions)
    print "training"
    svm_times = time_svm(combined_fingerprint_path, repetitions)

    min_times = [min(times) for times in [chunk_times, compute_fingerprint_times, combine_times, svm_times]]

    total_time = sum(min_times)

    accuracy = find_accuracy(combined_fingerprint_path)

    csv_writer.writerow([chunk_size] + min_times + [total_time, accuracy])

def repeat_eval():
    repetitions = 3
    chunk_sizes = [100000]
    for chunk_size in chunk_sizes:
        print "Trying chunk size %i" % (chunk_size)
        try:
            eval_chunk(chunk_size, repetitions)
            delete_files()
        except:
            delete_files()

def delete_files():
    root_path = 'data'
    for dirs in walkdir.dir_paths(walkdir.filtered_walk(root_path, excluded_dirs=['texts'])):
        if len(dirs.split('/'))>2:
            shutil.rmtree(dirs)
    for dir_name, _, files in walkdir.filtered_walk(root_path, excluded_dirs=['texts', 'model'], excluded_files=['.gitignore']):
        for file in files:
            file_path = os.path.join(dir_name, file)
            os.remove(file_path)

if __name__ == "__main__":
    print time.ctime()
    repeat_eval()
    print time.ctime()


