__author__ = 'eilidhhendry'

import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics
from sklearn.externals import joblib

def read_data(fingerprint_file):
    """
    Reads input file and creates matrix of numerical data and targets.
    :param fingerprint_file: input File (not string)
    :return: X_scaled - scaled matrix of input data, y - the target
    """
    # read the file into a pandas array
    data = pandas.read_csv(fingerprint_file, sep='\t', index_col=False)

    # get the numerical data
    num_data = data.ix[:,1:]

    # get the training data and the targets
    training_data = num_data.as_matrix().astype(numpy.float)
    target_data = data['target']
    # scale the data
    scaler = preprocessing.StandardScaler()
    training_data_scaled = scaler.fit_transform(training_data)
    return training_data_scaled, target_data

def test(test_file, clf):
    testing_data, testing_labels = read_data(test_file)

    # predict the test set
    test_outcomes = clf.predict(testing_data)

    # print the results
    for index, prediction in enumerate(test_outcomes):
        print index, 'target: ', testing_labels[index], 'pred: ', prediction
    """
    print 'hemingway: ', numpy.mean(test_outcome=='hemingway'), len([1 for item in test_outcome if item=='hemingway'])
    print 'nabokov: ', numpy.mean(test_outcome=='nabokov'), len([1 for item in test_outcome if item=='nabokov'])
    print 'steinbeck: ', numpy.mean(test_outcome=='steinbeck'), len([1 for item in test_outcome if item=='steinbeck'])
    print 'wallace:', numpy.mean(test_outcome=='wallace'), len([1 for item in test_outcome if item=='wallace'])
    """

def cross_validate_svm(classifier):
    print 'Best parameters set found on development set:'
    print classifier.best_params_

    y_true, y_pred = y_test, classifier.predict(X_test)
    print 'detailed class report:'
    print metrics.classification_report(y_true, y_pred)

    scores = cross_validation.cross_val_score(classifier, X_test, y_test, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# We train the SVM every time a new text/author is added to the system
def train_svm(training_file):
    # read in the training data
    X, y = read_data(training_file)

    #Split the data into training and validation set
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5, random_state=0)

    print "Feature space holds %d observations and %d features" % X_train.shape
    c_range = numpy.logspace(-2,2,40)

    print 'Tuning hyperparameters for precision'
    param_grid = [{'C': c_range, 'kernel': ['linear']}, {'C': c_range, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
    cv = 5
    scoring = "f1_weighted"

    clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=param_grid, cv=cv, scoring=scoring)
    clf.fit(X_train, y_train)

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

    model_output_file = "temp/model/model.pkl"
    store_classifier(clf, model_output_file)

    classifier = load_classifier(model_output_file)
    test(hemingway_test_file, classifier)
