# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC

import lexicon
from data import load3
from tokenizers import ExtendedWordTokenizer
from utils import classification_utils
from vectorizers import Lexicon2DVectorizer

data = load3()


def train(vectorizer, classifier):
    return classification_utils.train(data.train.data, data.train.labels,
                                      data.test.data, data.test.labels,
                                      vectorizer, classifier)


nb = MultinomialNB()
sgd = SGDClassifier(random_state=42)
lr = LogisticRegression(C=1000, random_state=42)
svm = LinearSVC(C=1000, random_state=42)

tfidf = TfidfVectorizer(ngram_range=(1, 2))
ext_tfidf = TfidfVectorizer(ngram_range=(1, 2), tokenizer=ExtendedWordTokenizer(), lowercase=False)
lex = Lexicon2DVectorizer(lexicon.full_lexicon)

print 'Naive Bayes'
print train(tfidf, nb)

print 'Naive Bayes, lexicon vectorizer'
print train(FeatureUnion([("lexicon", lex), ("tfidf", tfidf)]), nb)

print 'Naive Bayes, emoticons extraction'
print train(ext_tfidf, nb)

print 'Stochastic Gradient Descent'
print train(tfidf, sgd)

print 'Stochastic Gradient Descent, emoticons extraction'
print train(ext_tfidf, sgd)

print 'LogisticRegression'
print train(tfidf, lr)

print 'LogisticRegression, emoticons extraction'
print train(ext_tfidf, lr)

print 'SVM with linear kernel'
print train(tfidf, svm)

print 'SVM with linear kernel, emoticons extraction'
print train(ext_tfidf, svm)
