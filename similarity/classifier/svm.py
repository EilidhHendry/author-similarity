__author__ = 'eilidhhendry'

import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search
from sklearn.externals import joblib
import util

# surpress sklearn warnings about
import warnings

import constants

def scale(training_data):
    scaler = preprocessing.StandardScaler()
    training_data_scaled = scaler.fit_transform(training_data)
    return training_data_scaled


# We train the SVM every time a new text/author is added to the system
def train_svm(training_data, targets):
    """
    :param training_data: list of lists of floats representing fingerprint
    :param targets: list of strings representing target values (author name)
    """

    assert len(training_data) == len(targets), \
    'there are %r items in the target list and, but %r items in the list of training data' \
    % (len(targets), len(training_data))
    print "Training classifier with %s chunks" % (str(len(training_data)))

    try:
        #scale the input data
        scaled_training_data = scale(training_data)
    except ValueError as error:
        print 'no training data'
        print error
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        c_range = numpy.logspace(-2,2,40)

        print 'Tuning hyperparameters for precision'
        param_grid = [{'C': c_range, 'kernel': ['linear']}, {'C': c_range, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
        cv = 5
        scoring = "f1_weighted"

        clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=param_grid, cv=cv, scoring=scoring)

        clf.fit(training_data, targets)
        print "Trained classifier"

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
    #Split the data into training and validation set
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(training_data, targets, test_size=0.5, random_state=0)

    clf = train_svm(X_train, y_train)

    print 'Finding accuracy...'
    # find the accuracy of the classifier using 5-fold cross-validation
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5)

    # return the mean of the 5 folds
    return scores.mean()


def classify_single_fingerprint(fingerprint_dictionary, clf):
    """
    Classify test data using trained classifier. Prints list of lists containing probabilities.
    """
    fingerprint_list = util.dictionary_to_list(fingerprint_dictionary)
    # grab probabilities for each author which the classifier is trained on
    predicted_probabilities_ndarray = clf.predict_proba([fingerprint_list])[0]
    predicted_probabilities = predicted_probabilities_ndarray.tolist()
    labels = clf.best_estimator_.classes_.tolist()

    results = []
    for index in range(len(labels)):
        result = {
            "label": labels[index],
            "probability":  predicted_probabilities[index]
        }
        results.append(result)
    return results
