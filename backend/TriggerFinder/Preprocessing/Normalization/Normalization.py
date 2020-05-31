class Normalization:
    def __init__(self, inputFileList, outputFileList):
        if len(inputFileList) != len(outputFileList):
            raise Exception("File lists have different lengths")

        self.inputFileList = inputFileList
        self.outputFileList = outputFileList

    def normalize(self):
        for fileIndex in (0, len(self.inputFileList) - 1):
            file = open(self.inputFileList[fileIndex], "r")
            output = open(self.outputFileList[fileIndex], "w")
            if file and output:
                newContent = ''
                split = file.read().splitlines()
                for line in split:
                    newContent += self.normalizeSentence(line)
                    newContent += '\n'
                output.write(newContent)
                output.close()
                file.close()
            else:
                raise Exception("File does not exist")

    @staticmethod
    def normalizeSentence(sentence):
        newLine = ''
        for char in sentence.strip():
            if char.isalpha():
                newLine += char.lower()
            else:
                if char == ' ' or char == '\'':
                    newLine += char
        return newLine
