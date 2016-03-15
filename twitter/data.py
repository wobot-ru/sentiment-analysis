# -*- coding: utf-8 -*-
from sklearn.cross_validation import train_test_split
from sklearn.datasets.base import Bunch

from utils.io_utils import readlines


def load2():
    positives = readlines('../data/twitter/positive.txt')
    negatives = readlines('../data/twitter/negative.txt')

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


def load3():
    positives = readlines('../data/twitter/positive.txt')
    negatives = readlines('../data/twitter/negative.txt')
    neutrals = readlines('../data/twitter/neutral.txt')

    l = min(len(positives), len(negatives), len(neutrals))
    positives = positives[:l]
    negatives = negatives[:l]
    neutrals = neutrals[:l]

    data = positives + negatives + neutrals
    labels = ['POS'] * len(positives) + ['NEG'] * len(negatives) + ['NEUT'] * len(neutrals)

    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)

    return Bunch(
        train=Bunch(data=train_data, labels=train_labels),
        test=Bunch(data=test_data, labels=test_labels)
    )
