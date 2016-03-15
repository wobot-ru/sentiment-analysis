# -*- coding: utf-8 -*-
import numpy as np
import pymorphy2
from sklearn.base import BaseEstimator

from tokenizers import ExtendedWordTokenizer


class Lexicon2DVectorizer(BaseEstimator):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokenizer = ExtendedWordTokenizer(word_lower_case=False)

    def tokenize(self, doc):
        return self.tokenizer.tokenize(doc)

    def _get_sentiment(self, doc):
        tokens = [self.morph.parse(t)[0].normal_form for t in self.tokenize(doc)]
        positives = []
        negatives = []
        positive_score = 0.0
        negative_score = 0.0

        for token in tokens:
            if token in self.lexicon:
                rate = self.lexicon[token]
                if rate == 0:
                    continue
                if rate > 0:
                    positives.append(rate)
                if rate < 0:
                    negatives.append(-rate)

        if positives:
            positive_score = np.mean(positives)
        if negatives:
            negative_score = np.mean(negatives)

        return [positive_score, negative_score]

    def get_feature_names(self):
        return np.array(['pos', 'neg'])

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        return np.array([self._get_sentiment(doc) for doc in documents])

    def fit_transform(self, documents, y=None):
        return self.fit(documents).transform(documents)


class Lexicon1DVectorizer(BaseEstimator):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokenizer = ExtendedWordTokenizer()

    def tokenize(self, doc):
        return self.tokenizer.tokenize(doc)

    def _get_sentiment(self, doc):
        tokens = [self.morph.parse(t)[0].normal_form for t in self.tokenize(doc)]

        score = 0.00
        scores = []

        for token in tokens:
            if token in self.lexicon:
                scores.append(self.lexicon[token])

        if scores:
            score = np.mean(scores)

        return [score]

    def get_feature_names(self):
        return np.array(['sentiment'])

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        return np.array([self._get_sentiment(doc) for doc in documents])

    def fit_transform(self, documents,y=None):
        return self.fit(documents).transform(documents)


class Lexicon2DCountVectorizer(BaseEstimator):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokenizer = ExtendedWordTokenizer(word_lower_case=False)

    def tokenize(self, doc):
        return self.tokenizer.tokenize(doc)

    def _get_sentiment(self, doc):
        tokens = [self.morph.parse(t)[0].normal_form for t in self.tokenize(doc)]
        pos = 0
        neg = 0

        for token in tokens:
            if token in self.lexicon:
                rate = self.lexicon[token]
                if rate == 0:
                    continue
                if rate > 0:
                    pos += 1
                if rate < 0:
                    neg += 1

        return [pos, neg]

    def get_feature_names(self):
        return np.array(['pos', 'neg'])

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        return np.array([self._get_sentiment(doc) for doc in documents])

    def fit_transform(self, documents, y=None):
        return self.fit(documents).transform(documents)
