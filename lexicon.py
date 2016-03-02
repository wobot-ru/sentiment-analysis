# -*- coding: utf-8 -*-
import codecs


def load_lexicon():
    lines = codecs.open('./data/lexicon.txt', mode='r', encoding='utf-8').read().splitlines()
    return {k: float(v) for k, v in (line.split(';') for line in lines)}
