__author__ = 'eilidhhendry'

import argparse
import pandas
import numpy
from sklearn import preprocessing, cross_validation, svm, grid_search, metrics, feature_selection, pipeline
import matplotlib.pyplot as plot


def option_parser():
    """
    Parses command line options.
    Option to specify training file or testing file. Defaults provided.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--train-input", nargs='?', default="fingerprint_output/results.csv", type=argparse.FileType('r'),
                        help="File containing training data (default=feature_output/outputpos.txt)")
    parser.add_argument("-t", "--test-input", nargs='?', default="fingerprint_output/hemingway_imitation.txt", type=argparse.FileType('r'),
                        help="File containing test data (default=feature_output/outout_test_func2.txt)")
    args = parser.parse_args()
    return args


def read_data(in_file):
    """
    Reads input file and creates matrix of numerical data and targets.
    :param in_file: input File (not string)
    :return: X_scaled - scaled matrix of input data, y - the target
    """
    # read the file into a pandas array
    with open(in_file) as text:
        count = 1
        for line in text:
            word_count = 0
            if count == 3:
                break
            else:
                words = line.split('\t')
                for word in words:
                    print word
                    word_count += 1
                count +=1
                print word_count

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

def plot_confusion_matrix(cm, y, title='Confusion matrix', cmap=plot.cm.Blues):
    plot.imshow(cm, interpolation='nearest', cmap=cmap)
    plot.title(title)
    plot.colorbar()
    tick_marks = numpy.arange(len(numpy.unique(y)))
    plot.xticks(tick_marks, numpy.unique(y), rotation=45)
    plot.gca().invert_xaxis()
    plot.yticks(tick_marks, numpy.unique(y))
    plot.tight_layout()
    plot.ylabel('True label')
    plot.xlabel('Predicted label')


def test(test_file, clf):
    X_test, y_test = read_data(test_file)

    # predict the test set
    test_outcome = clf.predict(X_test)

    #test_outcome = cross_validation.cross_val_predict(clf, X_test, y_test, cv=5)

    # print the results
    if True:
        for index, prediction in enumerate(test_outcome):
            print index, 'target: ', y_test[index], 'pred: ', prediction

    print 'hemingway: ', numpy.mean(test_outcome=='hemingway'), len([1 for item in test_outcome if item=='hemingway'])
    print 'nabokov: ', numpy.mean(test_outcome=='nabokov'), len([1 for item in test_outcome if item=='nabokov'])
    print 'steinbeck: ', numpy.mean(test_outcome=='steinbeck'), len([1 for item in test_outcome if item=='steinbeck'])
    print 'wallace:', numpy.mean(test_outcome=='wallace'), len([1 for item in test_outcome if item=='wallace'])


    #print clf.predict_proba(X_test)
    #result = clf.decision_function(X_test)
    #print result
    #print result


def feature_selction_1(X_train, y_train, clf):

    # Create a feature-selection transform and an instance of SVM that we
    # combine together to have an full-blown estimator

    transform = feature_selection.SelectPercentile(feature_selection.f_classif)

    clf = pipeline.Pipeline([('anova', transform), ('svc', clf)])

    # Plot the cross-validation score as a function of percentile of features
    score_means = list()
    score_stds = list()
    percentiles = (1, 3, 6, 10, 15, 20, 30, 40, 60, 80, 100)

    for percentile in percentiles:
        clf.set_params(anova__percentile=percentile)
        this_scores = cross_validation.cross_val_score(clf, X_train, y_train)
        score_means.append(this_scores.mean())
        score_stds.append(this_scores.std())

    plot.errorbar(percentiles, score_means, numpy.array(score_stds))

    plot.title(
        'Performance of the SVM-Anova varying the percentile of features selected')
    plot.xlabel('Percentile')
    plot.ylabel('Prediction rate')

    plot.axis('tight')
    plot.show()

def feature_selection_2(X_train, y_train):
    X_indices = numpy.arange((X_train.shape[-1]))

    # Univariate feature selection with F-test for feature scoring
    # We use the default selection function: the 10% most significant features
    selector = feature_selection.SelectPercentile(feature_selection.f_classif, percentile=50)
    selector.fit(X_train, y_train)
    scores = -numpy.log10(selector.pvalues_)
    scores /= scores.max()
    plot.bar(X_indices - .45, scores, width=.2,
            label=r'Univariate score ($-Log(p_{value})$)', color='g')

    # Compare to the weights of an SVM
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    svm_weights = (clf.coef_ ** 2).sum(axis=0)
    svm_weights /= svm_weights.max()

    plot.bar(X_indices - .25, svm_weights, width=.2, label='SVM weight', color='r')

    clf_selected = svm.SVC(kernel='linear')
    clf_selected.fit(selector.transform(X_train), y_train)

    svm_weights_selected = (clf_selected.coef_ ** 2).sum(axis=0)
    svm_weights_selected /= svm_weights_selected.max()

    plot.bar(X_indices[selector.get_support()] - .05, svm_weights_selected,
            width=.2, label='SVM weights after selection', color='b')

    plot.title("Comparing feature selection")
    plot.xlabel('Feature number')
    plot.yticks(())
    plot.axis('tight')
    plot.legend(loc='upper right')
    plot.show()


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
    print 'Best parameters set found on development set:'
    print clf.best_params_
    print 'detailed class report:'

    y_true, y_pred = y_test, clf.predict(X_test)
    print metrics.classification_report(y_true, y_pred)

    scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    """
    f1_scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5, scoring='roc_auc')
    print("F1-Weighted: %0.2f (+/- %0.2f)" % (f1_scores.mean(), f1_scores.std() * 2))

    avg_precision_scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5, scoring='average_precision')
    print("F1-Weighted: %0.2f (+/- %0.2f)" % (avg_precision_scores.mean(), avg_precision_scores.std() * 2))
    """

    # calculate confusion matrix
    cm = metrics.confusion_matrix(y_true, y_pred)
    # normalise
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]
    # create plot of confusion matrix
    plot.figure()
    plot_confusion_matrix(cm_normalized, y_true, title='Normalized confusion matrix')
    plot.show()

    return clf

def train_svm2(training_file):
    # read in the training data
    X, y = read_data(training_file)

    #Split the data into training and validation set
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5, random_state=0)

    selector = feature_selection.SelectKBest(feature_selection.f_classif, k=1)
    pipe = pipeline.Pipeline([('selector', selector) , ('svm', svm.SVC(probability=True))])

    Crange = numpy.logspace(-2,2,40)
    print 'Tuning hyperparameters for precision'
    clf = grid_search.GridSearchCV(pipe, param_grid=[{'svm__C': Crange, 'svm__kernel': ['linear']}, {'svm__C': Crange, 'svm__gamma': [0.001, 0.0001], 'svm__kernel': ['rbf']}], cv=5, scoring='f1_weighted')
    clf.fit(X_train, y_train)
    print 'Best parameters set found on development set:'
    print clf.best_params_
    print 'detailed class report:'
    print 'k best features', selector.get_support(indices=True)



    y_true, y_pred = y_test, pipe.predict(X_test)
    print metrics.classification_report(y_true, y_pred)

    scores = cross_validation.cross_val_score(pipe, X_test, y_test, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    """
    f1_scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5, scoring='roc_auc')
    print("F1-Weighted: %0.2f (+/- %0.2f)" % (f1_scores.mean(), f1_scores.std() * 2))

    avg_precision_scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5, scoring='average_precision')
    print("F1-Weighted: %0.2f (+/- %0.2f)" % (avg_precision_scores.mean(), avg_precision_scores.std() * 2))
    """

    # calculate confusion matrix
    cm = metrics.confusion_matrix(y_true, y_pred)
    # normalise
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]
    # create plot of confusion matrix
    plot.figure()
    plot_confusion_matrix(cm_normalized, y_true, title='Normalized confusion matrix')
    plot.show()

    return clf

if __name__ == '__main__':
    training_file = "../fingerprint_output/training_fingerprints.csv"
    welch_test_file = "feature_output/split/all_welch_test.txt"
    hemingway_test_file ="../fingerprint_output/hemingway_imitation.txt"
    all_welch_test_file = "feature_output/final/all_welch.txt"
    clf = train_svm(training_file)


    print 'TEST ON HEMINGWAY DATASET'
    test(hemingway_test_file, clf)

    print 'TEST ON WELCH DATASET'
    test(welch_test_file, clf)

    print 'ALL WELCH'
    test(all_welch_test_file, clf)

