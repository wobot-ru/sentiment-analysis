# -*- coding: utf-8 -*-
import codecs
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion

from lexicon import load_lexicon
from vectorizers import LexiconVectorizer


def load_reviews(score):
    path = './data/otzovik/reviews/{0}/'.format(score)
    files = (fi for fi in os.listdir(path) if fi.endswith('_text.txt'))
    return [codecs.open(path + file_name, encoding='utf-8').read() for file_name in files]

neg_reviews = load_reviews(1) + load_reviews(2) + load_reviews(3)
pos_reviews = load_reviews(5)[:len(neg_reviews)]

half_neg = int(len(neg_reviews) * 0.75)
half_pos = int(len(pos_reviews) * 0.75)

neg_train = neg_reviews[half_neg:]
neg_test = neg_reviews[:half_neg]

pos_train = pos_reviews[half_pos:]
pos_test = pos_reviews[:half_pos]

train_set = neg_train + pos_train
labels = ['NEG'] * len(neg_train) + ['POS'] * len(pos_train)

tfidf_vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2), binary=False)
lexicon_vectorizer = LexiconVectorizer(lexicon = load_lexicon())
vectorizer = FeatureUnion([
    ("lexicon", lexicon_vectorizer),
    ("tfidf", tfidf_vectorizer)
])
classifier = MultinomialNB()
train_features = vectorizer.fit_transform(train_set)
classifier.fit(train_features, labels)

pos_test_features = vectorizer.transform(pos_test)
neg_test_features = vectorizer.transform(neg_test)

pos_predictions = classifier.predict(pos_test_features)
neg_predictions = classifier.predict(neg_test_features)

print np.mean(pos_predictions == 'POS')
print np.mean(neg_predictions == 'NEG')
