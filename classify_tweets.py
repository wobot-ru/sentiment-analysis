# -*- coding: utf-8 -*-
import codecs

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion

from lexicon import load_lexicon
from smiles import smiles_preprocessor
from vectorizers import LexiconVectorizer

all_neg_tweets = codecs.open('./data/tweets/negative.txt', encoding='utf-8').read().splitlines()
all_pos_tweets = codecs.open('./data/tweets/positive.txt', encoding='utf-8').read().splitlines()

half_neg = int(len(all_neg_tweets) * 0.5)
half_pos = int(len(all_pos_tweets) * 0.5)

neg_train = all_neg_tweets[half_neg:]
neg_test = all_neg_tweets[:half_neg]

pos_train = all_pos_tweets[half_pos:]
pos_test = all_pos_tweets[:half_pos]

train_set = neg_train + pos_train
labels = ['NEG'] * len(neg_train) + ['POS'] * len(pos_train)

tfidf_vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2), binary=False, preprocessor=smiles_preprocessor)
lexicon_vectorizer = LexiconVectorizer(lexicon=load_lexicon())
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

test_features = vectorizer.transform([
    u'Все козлы и пидарасы',
    u'Убить тебя мало',
    u'Ненавижу всех ублюдков',
    u'Я тебя люблю',
    u'Я в восторге',
    u'Пошел на хуй',
    u'Идите в жопу',
    ])
predictions = classifier.predict(test_features)
print predictions

