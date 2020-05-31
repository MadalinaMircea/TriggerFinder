from app import app, ensemble, predictSentenceEnsemble
from flask import request
import json


@app.route('/')
@app.route('/index')
def index():
    return "Welcome!"


# @app.route('/predictText', methods=['POST'])
# def predictText():
#     text = request.json['text']
#
#     print("Received text " + text)
#
#     newText = ""
#
#     startIndex = 0
#     endIndex = -1
#     wordCount = 0
#
#     maxN = 4
#
#     while startIndex < len(text) and endIndex < len(text) - 1:
#         endIndex += 1
#
#         if text[endIndex] == ' ' and endIndex > 0 and text[endIndex - 1] != ' ':
#             wordCount += 1
#
#         if wordCount == maxN:
#             value, sentence = predictSentence(w2v, model, text[startIndex:endIndex])
#             newText += sentence
#             wordCount = 0
#             startIndex = endIndex
#
#     if startIndex != len(text):
#         value, sentence = predictSentence(w2v, model, text[startIndex:])
#         newText += sentence
#
#     return json.dumps({"response": newText})


@app.route('/predictText', methods=['POST'])
def predictText():
    text = request.json['text']

    print("Received text " + text)

    newText = ""

    startIndex = 0
    endIndex = -1
    wordCount = 0
    oldNextIndex = 0
    nextIndex = 0

    maxN = 4
    while startIndex < len(text) and endIndex < len(text) - 1:
        endIndex += 1

        if text[endIndex] == '<' and endIndex < len(text) - 1 and text[endIndex + 1].isalpha():
            if startIndex < endIndex:
                value, sentence = predictSentenceEnsemble(ensemble, text[startIndex:endIndex])
                newText += sentence
            wordCount = 0
            nextIndex = 0

            startIndex = endIndex
            index = text[endIndex:].find('>')
            if index != -1:
                endIndex += index
                newText += text[startIndex:endIndex + 1]
                startIndex = endIndex + 1
            else:
                endIndex = startIndex
            continue

        if text[endIndex] == ' ' and endIndex > 0 and text[endIndex - 1] != ' ':
            wordCount += 1

        if wordCount == 2 and nextIndex == 0:
            nextIndex = endIndex

        if wordCount == maxN:
            value, sentence = predictSentenceEnsemble(ensemble, text[startIndex:endIndex])
            if value:
                newText += sentence
                startIndex = endIndex
            else:
                newText += text[startIndex:nextIndex]
                startIndex = nextIndex
                endIndex = startIndex
            # print(sentence)
            wordCount = 0
            nextIndex = 0

    if startIndex != len(text):
        value, sentence = predictSentenceEnsemble(ensemble, text[startIndex:])
        newText += sentence

    return json.dumps({"response": newText})
