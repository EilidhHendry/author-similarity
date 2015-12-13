__author__ = 'eilidhhendry'

import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics
from sklearn.externals import joblib

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


def train_csv(fingerprint_file):
    training_data, targets = read_csv(fingerprint_file)
    return train_svm(training_data, targets)


# We train the SVM every time a new text/author is added to the system
def train_svm(training_data, targets):

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

    return clf, X_test, y_test


def store_classifier(classifier, output_file_path):
    joblib.dump(classifier, output_file_path)


def load_classifier(classifier_file_path):
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
