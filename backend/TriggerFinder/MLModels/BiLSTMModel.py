from tensorflow.keras.layers import Input, Embedding
from tensorflow.keras.layers import Bidirectional, LSTM
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np


class BiLSTMModel:
    def __init__(self, info):
        self.best_weights_path = info.best_weights_path
        self.weights_path = info.weights_path

        if info.create:
            self.create_model(info.dimensions, info.embeddings, info.maxN, info.vocab, info.model_path)
        else:
            self.load_model(info.model_path, info.best_weights_path)

    def create_model(self, dimensions, embeddings, maxN, vocab, model_path):
        modelInput = Input(shape=(maxN,))
        model = Embedding(vocab, dimensions,
                          weights=[embeddings],
                          input_length=maxN,
                          trainable=False)(modelInput)
        model = Bidirectional(LSTM(units=100, return_sequences=True, dropout=0.25), merge_mode="concat")(model)
        model = Bidirectional(LSTM(units=100, return_sequences=True, dropout=0.5), merge_mode="concat")(model)
        model = TimeDistributed(Dense(100, activation="relu"))(model)
        model = Flatten()(model)
        model = Dense(100, activation="relu")(model)
        model = Dropout(rate=0.5)(model)
        model = Dense(25, activation="relu")(model)
        model = Dropout(rate=0.25)(model)
        out = Dense(2, activation="softmax")(model)

        self.model = Model(inputs=modelInput, outputs=out)

        self.model.save(model_path)

        # opt = Adam(learning_rate=0.00005)

        self.model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    def load_model(self, model_path, weights_path):
        self.model = load_model(model_path)
        self.model.compile(loss="mse",
                           optimizer="adam", metrics=["accuracy"])
        self.model.load_weights(weights_path)

    def predict(self, encoding):
        return self.model.predict(np.array(encoding))

    def fit(self, trainX, trainY):
        checkpoint = ModelCheckpoint(self.best_weights_path, verbose=1, monitor='val_loss',
                                     save_best_only=True, mode='auto')

        fit_history = self.model.fit(trainX, np.array(trainY), epochs=150, verbose=1, callbacks=[checkpoint],
                                     validation_split=0.25, shuffle=True)

        self.model.save_weights(self.weights_path)

        self.history = fit_history.history

        print("Done fitting")

    def evaluate(self, testX, testY):
        self.testHistory = self.model.evaluate(np.array(testX), np.array(testY), verbose=1)

    def writeHistory(self, loss_path, accuracy_path):
        content = ""
        for i in range(0, len(self.history["loss"])):
            content = content + str(i) + "," + str(self.history["loss"][i]) + '\n'

        loss_file = open(loss_path, "a+")
        loss_file.write(content)

        content = ""
        for i in range(0, len(self.history["accuracy"])):
            content = content + str(i) + "," + str(self.history["accuracy"][i]) + '\n'

        accuracy_file = open(accuracy_path, "a+")
        accuracy_file.write(content)

    def writeTestHistory(self, accuracy_path):
        content = ""
        for i in range(0, len(self.testHistory)):
            content = content + str(i) + "," + str(self.testHistory[i]) + '\n'

        accuracy_file = open(accuracy_path, "a+")
        accuracy_file.write(content)
