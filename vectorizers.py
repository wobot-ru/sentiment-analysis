# -*- coding: utf-8 -*-
import re

import numpy as np
import pymorphy2
from sklearn.base import BaseEstimator


class LexiconVectorizer(BaseEstimator):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.morph = pymorphy2.MorphAnalyzer()
        self.token_pattern = re.compile(r"(?u)\b\w\w+\b")

    def tokenize(self, doc):
        return self.token_pattern.findall(doc)

    def _get_sentiment(self, doc):
        tokens = [self.morph.parse(t)[0].normal_form for t in self.tokenize(doc)]
        pos_vals = []
        neg_vals = []
        avg_pos_val = 0
        avg_neg_val = 0

        for token in tokens:
            if token in self.lexicon:
                rate = self.lexicon[token]
                if rate == 0:
                    continue
                if rate > 0:
                    pos_vals.append(rate)
                if rate < 0:
                    neg_vals.append(-rate)

        if pos_vals:
            avg_pos_val = np.mean(pos_vals)
        if neg_vals:
            avg_neg_val = np.mean(neg_vals)

        return [avg_pos_val, avg_neg_val]

    def get_feature_names(self):
        return np.array(['pos', 'neg'])

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        return np.array([self._get_sentiment(doc) for doc in documents])
