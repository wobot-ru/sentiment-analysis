import pymorphy2

from lexicon import full_lexicon
from tokenizers import ExtendedWordTokenizer


class LexiconSentimentScorer(object):
    def __init__(self):
        self.lexicon = full_lexicon
        self.tokenizer = ExtendedWordTokenizer()
        self.morph = pymorphy2.MorphAnalyzer()

    def score(self, doc):
        tokens = [self.morph.parse(t)[0].normal_form for t in self.tokenizer.tokenize(doc)]
        scores = [self.lexicon[token] for token in tokens if token in self.lexicon]
        return float(sum(scores))