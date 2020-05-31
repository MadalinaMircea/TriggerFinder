class Information:
    def __init__(self, create, dimensions, embeddings, maxN, vocab, model_path, weights_path, best_weights_path):
        self.create = create
        self.dimensions = dimensions
        self.embeddings = embeddings
        self.maxN = maxN
        self.vocab = vocab
        self.model_path = model_path
        self.weights_path = weights_path
        self.best_weights_path = best_weights_path
