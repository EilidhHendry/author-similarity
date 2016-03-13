BASICALLY, 'preprocessing/compute_fingerprint.py' takes the training and testing data (including a tagged dataset for each) and creates csv files where the columns are features (avg. word length, etc.) and the rows are texts. These csv files are then passed to 'machine_learning/svm.py' which trains an svm on the training set and then tests it on the test set.

preprocessing/
  function_word_counts/
  compute_fingerprint.py
  compute_function_dist.py
  
Preprocessing directory contains functions used to create the lists of features required as input to the machine learning.
'compute_fingerprint.py' - finds the 'fingerprint' (list of features) for each text. Stores results as a csv file, in directory 'fingerprint_output', where the columns are features (average word length, etc) and the rows are texts.
'compute_function_dist.py' - is called upon by 'compute_fingerprint.py' to calculate the distributions of each function words. Stores required word counts in 'function_word_counts'.

REQUIRMENTS:
python packages: 
  nltk (incl. punkt tokeniser)
  sklearn
  numpy
  matplotlib
