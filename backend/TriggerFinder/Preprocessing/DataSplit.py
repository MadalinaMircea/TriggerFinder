class DataSplit:
    def __init__(self, data):
        self.data = data

    def split_data(self, folds):
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
