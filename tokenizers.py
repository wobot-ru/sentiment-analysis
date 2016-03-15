# -*- coding: utf-8 -*-
import re

import pymorphy2

import lexicon as lex


class RegexWordTokenizer(object):
    def __init__(self, lower_case=True):
        self.lower_case = lower_case
        # self.token_pattern = re.compile(r"(?u)\b[^\W]\w+\b")
        self.token_pattern = re.compile(r"(?u)\b\w\w+\b")

    def tokenize(self, doc):
        tokens = self.token_pattern.findall(doc)
        if self.lower_case:
            tokens = [x.lower() for x in tokens]
        return tokens

    def __call__(self, doc):
        return self.tokenize(doc)


class DictionaryTokenizer(object):
    def __init__(self, tokens, word_boundary=False, capture=False):
        tokens = tokens[:]
        tokens.sort(key=lambda w: len(w), reverse=True)
        tokens = [re.escape(word) for word in tokens]
        regex = '(?:' + "|".join(tokens) + ')'
        if word_boundary:
            regex = r"\b" + regex + r"\b"
        if capture:
            regex = '(' + regex + ')'
        self.token_pattern = re.compile(regex, flags=re.UNICODE)

    def tokenize(self, doc):
        return self.token_pattern.findall(doc)

    def __call__(self, doc):
        return self.tokenize(doc)


class ExtendedWordTokenizer(object):
    def __init__(self, word_lower_case=True):
        self.word_tokenizer = RegexWordTokenizer(lower_case=word_lower_case)
        self.emoticon_tokenizer = DictionaryTokenizer(tokens=lex.emoticons.keys(), word_boundary=False, capture=False)

    def tokenize(self, doc):
        return self.word_tokenizer.tokenize(doc) + self.emoticon_tokenizer.tokenize(doc)

    def __call__(self, doc):
        return self.tokenize(doc)


class LexiconTokenizer(object):
    def __init__(self):
        self.lexicon = lex.full_lexicon
        self.morph = pymorphy2.MorphAnalyzer()
        self.word_tokenizer = RegexWordTokenizer(lower_case=True)
        self.emoticon_tokenizer = DictionaryTokenizer(tokens=lex.emoticons.keys(), word_boundary=False, capture=False)

    def tokenize(self, doc):
        tokens = []
        words = self.word_tokenizer.tokenize(doc)
        words = [self.morph.parse(w)[0].normal_form for w in words]
        for w in words:
            if w in self.lexicon:
                tokens.append(w)

        tokens = tokens + self.emoticon_tokenizer.tokenize(doc)
        return tokens

    def __call__(self, doc):
        return self.tokenize(doc)