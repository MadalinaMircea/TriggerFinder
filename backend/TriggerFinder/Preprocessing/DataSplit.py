from sklearn.model_selection import StratifiedKFold


class DataSplit:
    def __init__(self, data):
        self.data = data

    def split_data(self, folds):
        # trainN = int((trainPercentage / 100) * len(self.data))
        # trainData = self.data[:trainN]
        # testData = self.data[trainN:]
        #
        # self.trainX, self.trainY = self.getDataAndLabels(trainData)
        # self.testX, self.testY = self.getDataAndLabels(testData)
        #
        # return self.trainX, self.trainY, self.testX, self.testY



        # X, Y = self.getDataAndLabels(self.data)
        #
        # kfold = StratifiedKFold(n_splits=folds, shuffle=True)
        #
        # train, test = kfold.split(X, Y)
        #
        # return X[train], Y[train], X[test], Y[test]

        self.K = folds
        self.splitData = []
        foldSize = int(len(self.data) / folds)

        for i in range(0, folds):
            self.splitData.append([])
            for j in range(0, foldSize):
                self.splitData[i].append(self.data[i * foldSize + j])

        return self.splitData

    def getFolds(self, fold):
        test = self.splitData[fold]
        train = []

        for f in range(0, self.K):
            if f != fold:
                train = train + self.splitData[f]

        return train, test


    @staticmethod
    def getDataAndLabels(lines):
        X = []
        Y = []

        for line in lines:
            lineSplit = line.split(',')
            X.append(lineSplit[0].strip())
            Y.append(int(lineSplit[1].strip()))

        return X, Y
