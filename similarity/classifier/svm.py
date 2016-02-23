__author__ = 'eilidhhendry'

import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics
from sklearn.externals import joblib
from sklearn.feature_selection import RFE
from sklearn.linear_model import RandomizedLogisticRegression
from sklearn.pipeline import Pipeline

# surpress sklearn warnings about
import warnings

import constants


def scale(training_data):
    scaler = preprocessing.StandardScaler()
    training_data_scaled = scaler.fit_transform(training_data)
    return training_data_scaled


def read_csv(fingerprint_file):
    """
    Reads input csv file and creates matrix of numerical data and targets.
    """

    # read the csv file into a pandas array
    data = pandas.read_csv(fingerprint_file, sep='\t', index_col=False)

    # get the numerical data
    num_data = data.ix[:,1:]

    # get the training data and the targets
    training_data = num_data.as_matrix()

    target_data = data['target'].tolist()

    return training_data, target_data


# We train the SVM every time a new text/author is added to the system
def train_svm(training_data, targets):
    """
    :param training_data: list of lists of floats representing fingerprint
    :param targets: list of strings representing target values (author name)
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        assert len(training_data) == len(targets), \
        'there are %r items in the target list and, but %r items in the list of training data' \
        % (len(targets), len(training_data))

        #scale the input data
        scaled_training_data = scale(training_data)

        c_range = numpy.logspace(-2,2,40)

        print 'Tuning hyperparameters for precision'
        param_grid = [{'C': c_range, 'kernel': ['linear']}, {'C': c_range, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
        cv = 5
        scoring = "f1_weighted"

        clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=param_grid, cv=cv, scoring=scoring)
        clf.fit(training_data, targets)

        return clf


def store_classifier(classifier, output_file_path=constants.MODEL_PATH):
    joblib.dump(classifier, output_file_path)


def load_classifier(classifier_file_path=constants.MODEL_PATH):
    classifier = joblib.load(classifier_file_path)
    return classifier


def find_classifier_accuracy(training_data, targets):
    """
    :param training_data: list of lists of floats representing fingerprint
    :param targets: list of strings representing target values (author name)
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        assert len(training_data) == len(targets), \
        'there are %r items in the target list and, but %r items in the list of training data' \
        % (len(targets), len(training_data))

        #scale the input data
        scaled_training_data = scale(training_data)

        #Split the data into training and validation set
        training_data, X_test, y_train, y_test = cross_validation.train_test_split(scaled_training_data, targets, test_size=0.5, random_state=0)

        print "Feature space holds %d observations and %d features" % training_data.shape
        c_range = numpy.logspace(-2,2,40)

        print 'Tuning hyperparameters for precision'
        param_grid = [{'C': c_range, 'kernel': ['linear']}, {'C': c_range, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]

        cv = 5
        scoring = "f1_weighted"
        clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=param_grid, cv=cv, scoring=scoring)
        clf.fit(training_data, y_train)

        # find the accuracy of the classifier using 5-fold cross-validation
        scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5)

        # return the mean of the 5 folds
        return scores.mean()


def classify(testing_data, clf):
    """
    Classify test data using trained classifier. Prints list of lists containing probabilities.
    """

    # grab probabilities for each author in the system
    test_probs = clf.predict_proba(testing_data)
    print test_probs


def evaluate_svm(classifier, test_data, test_targets):
    """
    Evaluates the svm on the task of author identification.
    Compares actual targets and predicted targets to find precision, recall and f-score.
    Also, uses k-fold cross-validation to find an accuracy for the classifier.

    :param classifier: a trained classifier
    :param test_data: matrix of numerical test data
    :param test_targets: list of the target author for each row in matrix
    """

    # list of actual targets for the test set, and get predicted targets using classifier
    actual_targets, predicted_targets = test_targets, classifier.predict(test_data)
    # compare actual targets and predicated targets
    print 'detailed class report:'
    print metrics.classification_report(actual_targets, predicted_targets)

    # use 5-fold cross validation to find average accuracy of classifier on test set
    scores = cross_validation.cross_val_score(classifier, test_data, test_targets, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


def svm_accuracy(classifier, test_data, test_targets):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # find the accuracy of the classifier using 5-fold cross-validation
        scores = cross_validation.cross_val_score(classifier, test_data, test_targets, cv=5)
        # return the mean of the 5 folds
        return scores.mean()
