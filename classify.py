#!/usr/bin/env python

'''
AuthorshipAttribution classify created by neil at 12/13/17 8:45 PM

Description: 
'''

import numpy as np
import pandas as pd
from sklearn import  decomposition, ensemble, linear_model, svm

class Classifier(object):

    def preprocess(self, a_feats, b_feats):
        dat = pd.concat([a_feats, b_feats], axis=0)
        self.labels = np.concatenate([np.zeros(len(a_feats)), np.ones(len(b_feats))])
        self.means = dat.mean()
        self.stds = dat.std()

        dat = (dat-self.means)/self.stds
        self.dat = dat

    def train(self):
        pass

    def predict(self, feats):
        dat = (feats - self.means)/self.stds
        #dat = self.pca.transform(dat)
        pred = self.model.predict(dat)
        return pred



class LogisticRegression(Classifier):

    def train(self):
        self.model = linear_model.LogisticRegressionCV()
        self.model.fit(self.dat, self.labels)


class SVM_RBF(Classifier):
    # hard to tune
    def train(self):
        self.model = svm.NuSVC()
        self.model.fit(self.dat, self.labels)

class LinearSVM(Classifier):
    def train(self):
        self.model = svm.LinearSVC()
        self.model.fit(self.dat, self.labels)

class AdaBoost(Classifier):
    def train(self):
        self.model = ensemble.AdaBoostClassifier()
        self.model.fit(self.dat, self.labels)