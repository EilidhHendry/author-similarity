__author__ = 'eilidhhendry'

import svm
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

input_file = 'feature_output/split/lda_shallow_hemingway.txt'
test_file = 'feature_output/final/readabilities_welch_test.txt'

def plot_2d(X, y, test='', clf='pca'):
    if clf=='pca':
        clf = PCA()
    if clf=='lda':
        clf = LDA()
    clf.n_components = 2
    X_reduced = clf.fit(X, y).transform(X)

    plt.figure()
    #plt.scatter(X_reduced[:,0], X_reduced[:,1])
    for i, row in enumerate(X_reduced):
        c = 'k'
        if y[i]=='hemingway':
            c = 'r'
        if y[i]=='nabokov':
            c = 'b'
        if y[i]=='steinbeck':
            c = 'g'
        if y[i]=='wallace':
            c = 'y'
        if y[i]=='hemingway_imitation':
            c='w'
        if i==0:
            plt.scatter(row[0], row[1], c=c, label='hemingway')
        if i==121:
            plt.scatter(row[0], row[1], c=c, label='nabokov')
        if i==350:
            plt.scatter(row[0], row[1], c=c, label='steinbeck')
        if i==465:
            plt.scatter(row[0], row[1], c=c, label='wallace')
        if i==620:
            plt.scatter(row[0], row[1], c=c, label='hemingway_imitation')
        else:
            plt.scatter(row[0], row[1], c=c)
    #for c, i, target_name in zip("rgby", [0,1,2,3], target_names):
    #    plt.scatter(X_reduced[i, 0], X_reduced[i, 1], c=c, label=target_name)
    plt.legend(loc=4)

    """
    result = []
    for line in test:
        result.append(clf.predict(line)[0])
    print result
    print 'hemingway: ', float(sum([1 for item in result if item=='hemingway']))/len(result)
    print 'nabokov: ', float(sum([1 for item in result if item=='nabokov']))/len(result)
    print 'steinbeck: ', float(sum([1 for item in result if item=='steinbeck']))/len(result)
    print 'wallace: ', float(sum([1 for item in result if item=='wallace']))/len(result)
    """
    plt.show()

def plot_3d_pca(X, y):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    pca = PCA(n_components=3)
    X_reduced = pca.fit(X).transform(X)

    for i, row in enumerate(X_reduced):
        c = ''
        if y[i]=='hemingway':
            c = 'r'
        if y[i]=='nabokov':
            c = 'b'
        if y[i]=='steinbeck':
            c = 'g'
        if y[i]=='wallace':
            c = 'y'
        ax.scatter(row[0], row[1], row[2], c=c)

    ax.set_xlabel('X Label')

    plt.show()

if __name__ =='__main__':
    X, y = svm.read_data(input_file)
    X_test, y_test = svm.read_data(test_file)
    plot_2d(X, y, clf='pca')
    #plot_3d_pca(X, y)
