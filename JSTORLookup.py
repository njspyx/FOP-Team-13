import json
import time

with open("fileInfo.json", "r") as rfi:
    fileInfo = json.load(rfi)

with open("wordIndex.json", "r") as rwi:
    wordIndex = json.load(rwi)

def JSTORWordLookup(wordList, numArticles): #assumes they are already set
    indexArrays = []
    frequencyChart = {}
    for word in wordList:
        if word in wordIndex:
            indexArrays.append(wordIndex[word])

    for list in indexArrays:
        for index in list:
            frequencyChart[index] = frequencyChart.get(index, 0) + 1

    bestArticles = sorted(frequencyChart, key=frequencyChart.get, reverse=True)
    for article in range(numArticles):
        print(bestArticles[article])
        print(fileInfo[bestArticles[article]][1])


wordList = ["beetle", "bicycle", "directions", "notes"]
JSTORWordLookup(wordList, 50)