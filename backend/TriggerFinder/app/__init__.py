from flask import Flask
from utils import get_model, predictSentence, predictSentenceEnsemble, readEnsemble
import os

app = Flask(__name__)

file = open(os.path.join(os.curdir, "Data/data_2.csv"))
d = file.read().splitlines()
model = "data_2 glove_100 bilstm stopwords no up CV epoch_100"
modelsP = os.path.join(os.curdir, "models", model)
accP = os.path.join(os.curdir, "metrics", model + "_acc.csv")
ensemble = readEnsemble(d, accP, modelsP)
w2v = ensemble.w2v
model = None

from app import routes
