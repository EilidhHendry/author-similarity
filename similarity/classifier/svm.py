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
def train_svm():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        training_data, targets = read_csv(constants.COMBINED_FINGERPRINT_FILE_PATH)

        #scale the input data
        scaled_training_data = scale(training_data)

        #Split the data into training and validation set
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(scaled_training_data, targets, test_size=0.5, random_state=0)

        print "Feature space holds %d observations and %d features" % X_train.shape
        c_range = numpy.logspace(-2,2,40)

        print 'Tuning hyperparameters for precision'
        param_grid = [{'C': c_range, 'kernel': ['linear']}, {'C': c_range, 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
        cv = 5
        scoring = "f1_weighted"

        clf = grid_search.GridSearchCV(svm.SVC(probability=True), param_grid=param_grid, cv=cv, scoring=scoring)
        clf.fit(X_train, y_train)
        """
        selector_svm = svm.SVC()
        selector_svm.set_params(C=clf.best_params_['C'], kernel = 'linear')
        selector = RFE(selector_svm, step=1)
        selector = selector.fit(X_train, y_train)
        print selector.support_
        print selector.ranking_

        pipe = Pipeline([('feature_selection', selector), ('classification', clf)])
        pipe.fit(X_train, y_train)

        return pipe, X_test, y_test
        """
        return clf, X_test, y_test

def store_classifier(classifier, output_file_path=constants.MODEL_PATH):
    joblib.dump(classifier, output_file_path)


def load_classifier(classifier_file_path=constants.MODEL_PATH):
    classifier = joblib.load(classifier_file_path)
    return classifier


def classify(test_file, clf):
    """
    Classify test data using trained classifier. Prints list of target and corresponding prediction.
    """

    # read csv file, split into numerical testing data and targets
    testing_data, targets = read_csv(test_file)

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


if __name__ == '__main__':
    # Parse combined finger print
    training_data, targets = read_csv(constants.COMBINED_FINGERPRINT_FILE_PATH)
    # Train the classifier
    clf, _, _ = train_svm(training_data, targets)
    # Store the classifier, and load again for fun
    store_classifier(clf, constants.MODEL_PATH)
    clf = load_classifier(constants.MODEL_PATH)

    # Make predictions about authorship
    test_path = "data/fingerprint_output/steinbeck/eastofeden/0002.csv"
    classify(test_path, clf)
