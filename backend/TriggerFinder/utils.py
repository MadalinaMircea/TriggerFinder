from Preprocessing.Embedding.Word2VecEmbedding import Word2VecEmbedding
from Preprocessing.DataShuffle import DataShuffle
from Preprocessing.DataSplit import DataSplit
from Preprocessing.Tokenization.TwitterTokenizer import TwitterTokenizer
from MLModels.BiLSTMModel import BiLSTMModel
from MLModels.Utils.Information import Information
from MLModels.Ensemble import Ensemble
from MLModels.Utils.EnsembleModel import EnsembleModel
import numpy as np
import os
from Preprocessing.Normalization.Normalization import Normalization
from math import sqrt
import matplotlib.pyplot as plt


def readEnsemble(data, accPath, modelPath):
    accFile = open(accPath, "r")
    accLines = accFile.readlines()
    line = accLines[0]
    i = 0

    w2v = Word2VecEmbedding(data, 100, os.path.join(os.curdir, "PretrainedUtils/w2v/w2v_100.pkl"))

    ensemble = Ensemble(w2v)

    while line.strip() != '':
        splitLine = line.split(',')
        modelNr = int(splitLine[0].strip()) - 1
        weight = float(splitLine[1].strip())
        modelP = os.path.join(modelPath, "bilstm_" + str(modelNr) + ".h5")
        weightsP = os.path.join(modelPath, "bilstm_" + str(modelNr) + "_weights.h5")

        ensemble.add_model(EnsembleModel(modelP, weightsP, w2v, weight))

        i += 1
        line = accLines[i]

    ensemble.load_all()

    return ensemble


def evaluate_ensemble(data, ensemble):
    f = open("ensemble_accuracies_2.csv", "w+")
    mse = 0
    rmse = 0
    mae = 0

    accurate = 0

    nr = 0

    for line in data:
        print("Line " + str(nr))
        splitLine = line.split(',')
        input = splitLine[0].strip()
        expected = int(splitLine[1].strip())
        normalized = Normalization.normalizeSentence(input)
        tokenized = []
        encoded = []
        if len(normalized) > 0:
            tokenized = TwitterTokenizer.tokenizeData([normalized])
            if len(tokenized) > 0:
                encoded = ensemble.w2v.getEncoding(tokenized)

        actual = ensemble.predict_all(encoded)

        mse += (expected - actual) ** 2
        mae += abs(expected - actual)

        if actual >= 0.5 and expected == 1:
            accurate += 1
        elif actual < 0.5 and expected == 0:
            accurate += 1

        nr += 1

    mse = mse / len(data)
    rmse = sqrt(mse)
    mae = mae / len(data)
    accuracy = accurate / len(data)

    content = "Mean squared error," + str(mse) + '\n'
    content = content + "Root mean squared error," + str(rmse) + '\n'
    content = content + "Mean absolute error," + str(mae) + '\n'
    content = content + "Accuracy," + str(accuracy)

    print(content)

    f.write(content)
    f.close()


def write_accuracies():
    finalContent = ''

    weightList = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3]

    metricsFolder = "metrics"

    for modelF in os.listdir(metricsFolder):
        modelFolder = os.curdir + "/" + metricsFolder + "/" + modelF

        newAccPath = modelFolder + "_acc.csv"
        newLossPath = modelFolder + "_loss.csv"

        accContent = ''
        lossContent = ''

        accFile = open(newAccPath, "w")
        lossFile = open(newLossPath, "w")

        index = 0

        accS = 0
        lossS = 0

        accList = []
        lossList = []

        for fileP in os.listdir(modelFolder):
            filePath = modelFolder + "/" + fileP
            if "test" in fileP:
                index += 1
                file = open(filePath, "r")
                lines = file.readlines()
                loss = lines[0].split(',')[1].strip()
                acc = lines[1].split(',')[1].strip()
                # accContent = accContent + str(index) + "," + acc + '\n'
                # lossContent = lossContent + str(index) + "," + loss + '\n'
                file.close()

                accList.append([index, float(acc)])
                lossList.append([index, float(loss)])
                # accS += float(acc)
                # lossS += float(loss)

        accList.sort(key=lambda x: x[1])
        lossList.sort(key=lambda x: x[1])

        for i in range(0, len(accList)):
            accS += weightList[i] * accList[i][1]
            lossS += weightList[i] * lossList[i][1]
            accContent = accContent + str(accList[i][0]) + "," + str(weightList[i]) + ',' + str(accList[i][1]) + '\n'
            lossContent = lossContent + str(lossList[i][0]) + "," + str(weightList[i]) + ',' + str(
                lossList[i][1]) + '\n'

        finalAcc = accS / 2
        finalLoss = lossS / 2

        accContent = accContent + '\nTotal,,' + str(finalAcc)
        lossContent = lossContent + '\nTotal,,' + str(finalLoss)

        accFile.write(accContent)
        lossFile.write(lossContent)

        finalContent = finalContent + modelF + "," + str(finalAcc) + "," + str(finalLoss) + '\n'

        accFile.close()
        lossFile.close()

    print(finalContent)


def predictSentenceEnsemble(ensemble, sentence):
    value = 0
    normalized = Normalization.normalizeSentence(sentence)
    if len(normalized) > 0:
        tokenized = TwitterTokenizer.tokenizeData([normalized])
        if len(tokenized) > 0:
            encoded = ensemble.w2v.getEncoding(tokenized)
            value = ensemble.predict_all(encoded)

    result = ""

    if value >= 0.5:
        for letter in sentence:
            if letter.isalpha():
                result += '*'
            else:
                result += letter
        return True, result
    else:
        return False, sentence


def predictSentence(w2v, model, sentence):
    value = 0
    normalized = Normalization.normalizeSentence(sentence)
    if len(normalized) > 0:
        tokenized = TwitterTokenizer.tokenizeData([normalized])
        if len(tokenized) > 0:
            encoded = w2v.getEncoding(tokenized)
            value = model.predict(encoded)[0][0]

    result = ""

    if value >= 0.5:
        for letter in sentence:
            if letter.isalpha():
                result += '*'
            else:
                result += letter
        return True, result
    else:
        return False, sentence


def get_model():
    file = open(os.path.join(os.curdir, "Data/data_2.csv"))
    if file:
        data = file.read().splitlines()

        w2v = Word2VecEmbedding(data, 100, os.path.join(os.curdir, "PretrainedUtils/w2v/w2v_100.pkl"))

        model_path = os.path.join(os.curdir, "models/bilstm_0.h5")
        best_weights_path = os.path.join(os.curdir, "models/bilstm_0_best_weights.h5")

        info = Information(False, w2v.dimensions, w2v.embeddings, w2v.max_N, w2v.vocab_N, model_path, best_weights_path,
                               best_weights_path)

        model = BiLSTMModel(info)

        return w2v, model


def cross_validation():
    file = open(os.path.join(os.curdir, "Data/data_2.csv"))
    if file:
        data = file.read().splitlines()

        w2v = Word2VecEmbedding(data, 100, os.path.join(os.curdir, "PretrainedUtils/w2v/w2v_100.pkl"))

        data = DataShuffle.shuffle(data)

        K = 10

        split = DataSplit(data)
        splitData = split.split_data(K)

        for fold in range(0, K):
            model_path = os.path.join(os.curdir, "models/bilstm_" + str(fold) +".h5")
            best_weights_path = os.path.join(os.curdir, "models/bilstm_" + str(fold) +"_best_weights.h5")
            weights_path = os.path.join(os.curdir, "models/bilstm_" + str(fold) +"_weights.h5")

            if os.path.exists(model_path) and os.path.exists(weights_path):
                print("Model and weights files exist")
                info = Information(False, w2v.dimensions, w2v.embeddings, w2v.max_N, w2v.vocab_N, model_path, weights_path,
                                   best_weights_path)
            else:
                print("Model and weights do not exist")
                info = Information(True, w2v.dimensions, w2v.embeddings, w2v.max_N, w2v.vocab_N, model_path, weights_path,
                                   best_weights_path)

            model = BiLSTMModel(info)

            print("Fold " + str(fold))
            train, test = split.getFolds(fold)
            trainX, trainY = split.getDataAndLabels(train)
            testX, testY = split.getDataAndLabels(test)

            trainY = [[0, 1] if x == 0 else [1, 0] for x in trainY]
            testY = [[0, 1] if x == 0 else [1, 0] for x in testY]

            # tokenized_train = TwitterTokenizer.tokenizeData(trainX)
            encoded_train = w2v.getEncoding(trainX)

            # tokenized_test = TwitterTokenizer.tokenizeData(testX)
            encoded_test = w2v.getEncoding(testX)

            model.fit(encoded_train, np.array(trainY))

            model.evaluate(encoded_test, testY)

            model.writeHistory("metrics/bilstm_" + str(fold) +"_loss.csv", "metrics/bilstm_" + str(fold) +"_accuracy.csv")

            model.writeTestHistory("metrics/bilstm_test_accuracy_" + str(fold) + ".csv")


def write_accuracies():
    finalContent = ''

    weightList = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3]

    metricsFolder = "metrics"

    for modelF in os.listdir(metricsFolder):
        modelFolder = os.curdir + "/" + metricsFolder + "/" + modelF

        newAccPath = modelFolder + "_acc.csv"
        newLossPath = modelFolder + "_loss.csv"

        accContent = ''
        lossContent = ''

        accFile = open(newAccPath, "w")
        lossFile = open(newLossPath, "w")

        index = 0

        accS = 0
        lossS = 0

        accList = []
        lossList = []

        for fileP in os.listdir(modelFolder):
            filePath = modelFolder + "/" + fileP
            if "test" in fileP:
                index += 1
                file = open(filePath, "r")
                lines = file.readlines()
                loss = lines[0].split(',')[1].strip()
                acc = lines[1].split(',')[1].strip()
                # accContent = accContent + str(index) + "," + acc + '\n'
                # lossContent = lossContent + str(index) + "," + loss + '\n'
                file.close()

                accList.append([index, float(acc)])
                lossList.append([index, float(loss)])
                # accS += float(acc)
                # lossS += float(loss)

        accList.sort(key=lambda x: x[1])
        lossList.sort(key=lambda x: x[1])

        for i in range(0, len(accList)):
            accS += weightList[i] * accList[i][1]
            lossS += weightList[i] * lossList[i][1]
            accContent = accContent + str(accList[i][0]) + "," + str(weightList[i]) + ',' + str(accList[i][1]) + '\n'
            lossContent = lossContent + str(lossList[i][0]) + "," + str(weightList[i]) + ',' + str(
                lossList[i][1]) + '\n'

        finalAcc = accS / 2
        finalLoss = lossS / 2

        accContent = accContent + '\nTotal,,' + str(finalAcc)
        lossContent = lossContent + '\nTotal,,' + str(finalLoss)

        accFile.write(accContent)
        lossFile.write(lossContent)

        finalContent = finalContent + modelF + "," + str(finalAcc) + "," + str(finalLoss) + '\n'

        accFile.close()
        lossFile.close()

    print(finalContent)


def plot_csv_files(path):
    for f in os.listdir(path):
        if "loss" in f:
            filePath = os.path.join(path, f)
            file = open(filePath, "r")
            X = []
            Y = []
            for line in file.readlines():
                splitLine = line.split(',')
                X.append(int(splitLine[0].strip()))
                Y.append(float(splitLine[1].strip()))

            plt.plot(X, Y)
    plt.show()
