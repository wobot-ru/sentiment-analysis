# -*- coding: utf-8 -*-
from sklearn.cross_validation import train_test_split
from sklearn.datasets.base import Bunch

from utils.io_utils import readlines


def load():
    positives = readlines('../data/tweets/positive.txt')
    negatives = readlines('../data/tweets/negative.txt')

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