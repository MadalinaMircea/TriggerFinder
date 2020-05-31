from MLModels.Utils.Information import Information
from MLModels.BiLSTMModel import BiLSTMModel


class EnsembleModel:
    def __init__(self, modelPath, weightsPath, w2v, weight):
        self.modelPath = modelPath
        self.weightsPath = weightsPath
        self.w2v = w2v
        self.model = None
        self.weight = weight

    def load(self):
        info = Information(False, self.w2v.dimensions, self.w2v.embeddings,
                           self.w2v.max_N, self.w2v.vocab_N, self.modelPath, self.weightsPath,
                           self.weightsPath)

        self.model = BiLSTMModel(info)

        print(self.model.model.summary())

        return self.model

    def predict(self, encoded):
        return self.model.predict(encoded)[0][0]
