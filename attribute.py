#!/usr/bin/env python

'''
AuthorshipAttribution attribute created by neil at 12/14/17 2:43 PM

Description:
handel calls from UI
'''

import numpy as np

import classify
import features

class AuthorAttribute(object):

    def identify(self, author_files):
        self.author_features = dict()
        self.authors = list()
        for author, files in author_files.items():
            fe = features.FeatureExtractor(5000)
            self.author_features[author] = fe.analyze_texts(files)
            self.authors.append(author)
            #import pdb
            #pdb.set_trace()

        #self.classifier = classify.LogisticRegression()
        #self.classifier = classify.SVM_RBF()
        #self.classifier = classify.LinearSVM()
        self.classifier = classify.AdaBoost()
        self.classifier.preprocess(self.author_features[self.authors[0]],
                                   self.author_features[self.authors[1]])
        self.classifier.train()


    def attribute(self, files):
        authors = dict()
        for file in files:
            fe = features.FeatureExtractor(np.inf)
            feats = fe.analyze_texts([file])
            pred = self.classifier.predict(feats)
            authors[file] = self.authors[int(pred[0])]

        #for file, author in authors.items():
        #    print("%s Author: %s"%(file, author))

        return authors