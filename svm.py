__author__ = 'eilidhhendry'

import argparse
import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics, feature_selection, pipeline
from sklearn.externals import joblib

def read_data(in_file):
    """
    Reads input file and creates matrix of numerical data and targets.
    :param in_file: input File (not string)
    :return: X_scaled - scaled matrix of input data, y - the target
    """
    # read the file into a pandas array
    data = pandas.read_csv(in_file, sep='\t', index_col=False)
    print data

    # get the numerical data
    num_data = data.ix[:,1:]

    # get the training data (X) and the targets (y)
    X = num_data.as_matrix().astype(numpy.float)
    y = data['target']
    # scale the data
    scaler = preprocessing.StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

def test(test_file, clf):
    X_test, y_test = read_data(test_file)

    # predict the test set
    test_outcome = clf.predict(X_test)

    # print the results
    for index, prediction in enumerate(test_outcome):
        print index, 'target: ', y_test[index], 'pred: ', prediction

    print 'hemingway: ', numpy.mean(test_outcome=='hemingway'), len([1 for item in test_outcome if item=='hemingway'])
    print 'nabokov: ', numpy.mean(test_outcome=='nabokov'), len([1 for item in test_outcome if item=='nabokov'])
    print 'steinbeck: ', numpy.mean(test_outcome=='steinbeck'), len([1 for item in test_outcome if item=='steinbeck'])
    print 'wallace:', numpy.mean(test_outcome=='wallace'), len([1 for item in test_outcome if item=='wallace'])

def train_svm(training_file):
    # read in the training data
    X, y = read_data(training_file)

    #Split the data into training and validation set
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5, random_state=0)

    print "Feature space holds %d observations and %d features" % X_train.shape
    Crange = numpy.logspace(-2,2,40)

    print 'Tuning hyperparameters for precision'
    clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=[{'C': Crange, 'kernel': ['linear']}, {'C': Crange, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}], cv=5, scoring='f1_weighted')
    clf.fit(X_train, y_train)
    """
    print 'Best parameters set found on development set:'
    print clf.best_params_
    print 'detailed class report:'

    y_true, y_pred = y_test, clf.predict(X_test)
    print metrics.classification_report(y_true, y_pred)

    scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    """

    return clf

def store_classifier(classifier, output_file_path):
    joblib.dump(classifier, output_file_path)

def load_classifier(classifier_file_path):
    classifier = joblib.load(classifier_file_path)
    return classifier

if __name__ == '__main__':
    training_file = "temp/fingerprint_output/training_fingerprints.csv"
    hemingway_test_file ="temp/fingerprint_output/hemingway_imitation.csv"
    clf = train_svm(training_file)

    model_output_file = "temp/models/model.pkl"
    store_classifier(clf, model_output_file)

    classifier = load_classifier(model_output_file)
    test(hemingway_test_file, classifier)
