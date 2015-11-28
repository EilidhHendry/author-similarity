__author__ = 'eilidhhendry'

import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics
from sklearn.externals import joblib


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
    training_data = num_data.as_matrix().astype(numpy.float)
    target_data = data['target']

    return target_data, training_data


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

    # predict the test set
    test_outcomes = clf.predict(testing_data)

    # print the results
    for index, prediction in enumerate(test_outcomes):
        print index, 'target: ', targets[index], 'pred: ', prediction
    """
    print 'hemingway: ', numpy.mean(test_outcome=='hemingway'), len([1 for item in test_outcome if item=='hemingway'])
    print 'nabokov: ', numpy.mean(test_outcome=='nabokov'), len([1 for item in test_outcome if item=='nabokov'])
    print 'steinbeck: ', numpy.mean(test_outcome=='steinbeck'), len([1 for item in test_outcome if item=='steinbeck'])
    print 'wallace:', numpy.mean(test_outcome=='wallace'), len([1 for item in test_outcome if item=='wallace'])
    """

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
    read_csv("data/fingerprint_output/training_fingerprints.csv")

    """
    training_file = "data/fingerprint_output/training_fingerprints.csv"
    hemingway_test_file ="data/fingerprint_output/hemingway_imitation.csv"
    clf = train_svm(training_file)

    model_output_file = "data/model/model.pkl"
    store_classifier(clf, model_output_file)

    classifier = load_classifier(model_output_file)
    test(hemingway_test_file, classifier)
    """
