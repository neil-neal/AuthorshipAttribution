#!/usr/bin/env python

'''
AuthorshipAttribution feature_extraction created by neil at 12/13/17 2:55 PM

Description: 
'''

import glob
import nltk
import numpy as np
import pandas as pd
import re

class FeatureExtractor(object):

    def __init__(self, len):
        self.paragraph_length = len # in characters
        self.function_words = ['and', 'or', 'not', 'but', 'since'
            , 'will', 'would', 'shall', 'should'
            , 'as', 'upon', 'on', 'by', 'of', 'with','the'
            , 'it', 'you', 'i', 'he', 'she', 'they', 'we'
            , 'her', 'his', 'my', 'its', 'their', 'our', 'your'
            , 'me', 'him', 'us', 'them'
                          ]
        self.key_punctuations = [';', ':', ',', '"']
        self.pos_list = ['NN', 'NNP', 'DT', 'IN', 'JJ', 'NNS']

    def extract(self, paragraph):
        paragraph = paragraph.lower()
        sentences = paragraph.split('.')
        #import pdb
        #pdb.set_trace()
        words = re.sub('[^a-zA-Z]+', ' ', paragraph) # keep only characters
        words = words.split()

        sentence_count = len(sentences)
        word_count = len(words)
        char_count = np.sum([len(word) for word in words])

        #print("sc: %d wc: %d cc: %d"%(sentence_count, word_count, char_count))

        features = dict()
        features['words/sntnc'] = word_count/sentence_count
        features['chars/sntnc'] = char_count/sentence_count
        features['chars/word'] = char_count/word_count

        for punc in self.key_punctuations:
            count = paragraph.count(punc)
            features['%s/sntnc'%punc] = count/sentence_count

        for word in self.function_words:
            features[word+'%'] = words.count(word)/word_count*100

        poses = nltk.word_tokenize(paragraph.lower())
        poses = [p[1] for p in nltk.pos_tag(poses)]
        for pos in self.pos_list:
            features["%s/word"%pos] = poses.count(pos)/word_count
        return pd.Series(features)


    def analyze_texts(self, flnms):
        features = []
        paragraph = ''
        for flnm in flnms:
            with open(flnm, 'r') as fl:
                for line in fl:
                    sentences = line.split('.')
                    for sntnc in sentences:
                        if len(paragraph) < self.paragraph_length:
                            paragraph += ' ' + sntnc + '.'
                        else:
                            features.append(self.extract(paragraph))
                            paragraph = ''

            if not np.isfinite(self.paragraph_length): # each file is a paragraph
                features.append(self.extract(paragraph))
                paragraph = ''

        return pd.DataFrame(features)


def tester():
    fe = FeatureExtractor(2000)
    #files = ['text/federalist_papers/1_Hamilton', 'text/federalist_papers/6_Hamilton']
    #files = glob.glob('text/federalist_papers/*[0-9]_Madison')
    files = glob.glob('text/federalist_papers/*[0-9]_Hamilton')

    return fe.analyze_texts(files)