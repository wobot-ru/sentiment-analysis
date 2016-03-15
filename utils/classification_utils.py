# -*- coding: utf-8 -*-
from sklearn import metrics
from sklearn.pipeline import Pipeline


def train(train_data, train_labels, test_data, test_labels, vectorizer, classifier):
    model = Pipeline([('vect', vectorizer), ('clf', classifier)])
    model.fit(train_data, train_labels)
    predicted_labels = model.predict(test_data)
    return metrics.classification_report(test_labels, predicted_labels, digits=3)
