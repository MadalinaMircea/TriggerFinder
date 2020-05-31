from Preprocessing.Lemmatization.Lemmatizer import Lemmatizer
from nltk.corpus import wordnet as wn


class WordnetLemmatizer(Lemmatizer):
    def __init__(self):
        """constructor"""

    def lemmatizeWordList(self, wordList):
        result = []
        for word in wordList:
            result.append(self.lemmatizeWord(word))
        return result

    def lemmatizeWord(self, word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma