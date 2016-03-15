# -*- coding: utf-8 -*-
import codecs


def fopen(filename, mode='r'):
    return codecs.open(filename, mode=mode, encoding='utf-8')


def readlines(filename):
    result = []
    for line in fopen(filename):
        line = line.strip()
        if line:
            result.append(line)
    return result
