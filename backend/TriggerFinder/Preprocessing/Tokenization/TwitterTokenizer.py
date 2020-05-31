from Preprocessing.Tokenization.Tokenizer import Tokenizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from Preprocessing.Lemmatization.WordnetLemmatizer import WordnetLemmatizer


class TwitterTokenizer(Tokenizer):
    def __init__(self):
        # nltk.download('wordnet')
        # nltk.download('stopwords')
        super().__init__()
        self.stopwords = set(stopwords.words('english'))
        self.stopwords.remove("up")
        self.tokenizer = TweetTokenizer()
        self.lemmatizer = WordnetLemmatizer()

    def tokenize(self, sentence):
        tokens = self.tokenizer.tokenize(sentence)
        # tokens = [token for token in tokens if (token not in self.stopwords and len(token) > 1)]
        tokens = [token for token in tokens if (len(token) > 1)]
        return self.lemmatizer.lemmatizeWordList(tokens)

    @staticmethod
    def tokenizeData(data):
        result = []
        tokenizer = TwitterTokenizer()
        for line in data:
            inputData = line.split(',')[0]
            result.append(tokenizer.tokenize(inputData))
        return result
