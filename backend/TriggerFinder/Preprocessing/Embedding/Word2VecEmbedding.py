from Preprocessing.Embedding.Embedding import Embedding
from Preprocessing.Tokenization.TwitterTokenizer import TwitterTokenizer
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from numpy import zeros
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Word2VecEmbedding(Embedding):
    def __init__(self, data, dimensions, w2vPath):
        super().__init__()
        self.dimensions = dimensions
        tokenized_data = TwitterTokenizer.tokenizeData(data)
        # print(tokenized_data)
        self.max_N = self.get_max_N(tokenized_data)
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(data)
        self.vocab_N = len(self.tokenizer.word_index) + 1
        self.word2vec = self.get_word2vec(w2vPath)
        self.embeddings = self.getEmbeddings()

    def get_word2vec(self, path):
        return pickle.load(open(path, "rb"))

    def get_max_N(self, tokenized_data):
        max_N = 0
        for sentence in tokenized_data:
            n = len(sentence)
            if n > max_N:
                max_N = n

        return max_N

    def getEmbeddings(self):
        embeddings = zeros((self.vocab_N, self.dimensions))
        for word, index in self.tokenizer.word_index.items():
            vector = self.word2vec.get(word)
            if vector is not None:
                embeddings[index] = vector
        return embeddings

    def getEncoding(self, sentenceList):
        encoded_docs = self.tokenizer.texts_to_sequences(sentenceList)
        return pad_sequences(encoded_docs, maxlen=self.max_N, padding="post")
