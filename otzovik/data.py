# -*- coding: utf-8 -*-
from sklearn.cross_validation import train_test_split
from sklearn.datasets.base import Bunch

from utils.io_utils import readlines


def load_reviews(score):
    return readlines('../data/otzovik/{0}_text.txt'.format(score))


def load():
    negatives = load_reviews(1) + load_reviews(2) + load_reviews(3)
    positives = load_reviews(5)

    l = min(len(positives), len(negatives))
    positives = positives[:l]
    negatives = negatives[:l]

    data = positives + negatives
    labels = ['POS'] * len(positives) + ['NEG'] * len(negatives)

    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)

    return Bunch(
        train=Bunch(data=train_data, labels=train_labels),
        test=Bunch(data=test_data, labels=test_labels)
    )
