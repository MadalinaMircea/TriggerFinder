class Merging:
    def __init__(self, fileValueList):
        self.fileValueList = fileValueList

    def merge(self, outputFile):
        output = open(outputFile, "w")
        content = ''
        if output:
            for fileIndex in (0, len(self.fileValueList) - 1):
                file = open(self.fileValueList[fileIndex][0], "r")
                value = str(self.fileValueList[fileIndex][1])
                if file:
                    for line in file.read().splitlines():
                        content = content + line.strip() + ',' + value + '\n'
                    file.close()
                else:
                    output.close()
                    raise Exception("Input file does not exist")
        else:
            raise Exception("Output file does not exist")
        output.write(content)
        output.close()