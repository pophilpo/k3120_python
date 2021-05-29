from collections import defaultdict
from math import log
from statistics import mean


class NaiveBayesClassifier:
    def __init__(self, a: int = 1e-5):
        self.d = 0
        self.word = defaultdict(lambda: 0)
        self.classified_words = defaultdict(lambda: 0)
        self.classes = defaultdict(lambda: 0)
        self.a = a

    def fit(self, X, y):

        for xi, yi in zip(X, y):
            self.classes[yi] += 1

            words = xi.split()
            for w in words:
                self.word[w] += 1
                self.classified_words[w, yi] += 1

        for c in self.classes:
            self.classes[c] /= len(X)

        self.d = len(self.word)

    def predict(self, feature):

        def formul(self, cls, word):
            return log(
                (self.classified_words[word, cls] + self.a) /
                (self.word[word] + self.a * self.d)
            )

        def class_probability(self, cls, feature):
            return log(self.classes[cls]) + sum(formul(self, cls, w) for w in feature.split())

        return max(self.classes.keys(), key=lambda c: class_probability(self, c, feature))

    def _get_predictions(self, dataset):
        return [self.predict(feature) for feature in dataset]

    def score(self, dataset, classes):
        predictions = self._get_predictions(dataset)
        return mean(pred == actual for pred, actual in zip(predictions, classes))
