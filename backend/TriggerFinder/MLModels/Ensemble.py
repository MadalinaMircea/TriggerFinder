from MLModels.Utils.EnsembleModel import EnsembleModel
import threading


class Ensemble:
    def __init__(self, w2v):
        self.models = []
        self.w2v = w2v
        self.lock = threading.Lock()
        self.result = 0

    def add_model(self, model):
        self.models.append(model)

    def load_all(self):
        for m in self.models:
            m.load()
        # thread_1 = threading.Thread(target=self.thread_load, args=(self.models[0:3],))
        # thread_1.start()
        # thread_2 = threading.Thread(target=self.thread_load, args=(self.models[3:6],))
        # thread_2.start()
        # thread_3 = threading.Thread(target=self.thread_load, args=(self.models[6:],))
        # thread_3.start()
        # thread_1.join()
        # thread_2.join()
        # thread_3.join()

    @staticmethod
    def thread_load(models):
        for m in models:
            m.load()

    def predict_all(self, encoded):
        self.result = 0
        thread_1 = threading.Thread(target=self.thread_predict, args=(self.models[0:3], encoded))
        thread_1.start()
        thread_2 = threading.Thread(target=self.thread_predict, args=(self.models[3:6], encoded))
        thread_2.start()
        thread_3 = threading.Thread(target=self.thread_predict, args=(self.models[6:], encoded))
        thread_3.start()
        thread_1.join()
        thread_2.join()
        thread_3.join()
        return self.result / 2

    def thread_predict(self, models, encoded):
        result = 0
        for m in models:
            result += m.weight * m.predict(encoded)
        self.lock.acquire()
        self.result += result
        self.lock.release()
