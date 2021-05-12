import json
import time

with open("fileInfo.json", "r") as rfi:
    fileInfo = json.load(rfi)
rfi.close()

with open("wordIndex.json", "r") as rwi:
    wordIndex = json.load(rwi)
rwi.close()

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
        print("Index of paper: " + str(bestArticles[article]))
        print("Number of word appearances: " + str(frequencyChart[bestArticles[article]]))
        print("File name: " + fileInfo[bestArticles[article]][0])
        try:
            print("Title: " + fileInfo[bestArticles[article]][1])
        except TypeError:
            print("No Title")

        try:
            print("URL: " + fileInfo[bestArticles[article]][2])
        except TypeError:
            print("No URL")

        try:
            print("Abstract: " + fileInfo[bestArticles[article]][3])
        except TypeError:
            print("No Abstract")

        try:
            print("Authors: ", end="")
            authorList = fileInfo[bestArticles[article]][4]
            numAuthors = len(authorList)
            for author in range(numAuthors):
                if author == numAuthors-1:
                    print(authorList[author])
                else:
                    print(authorList[author], end=", ")
        except TypeError:
            print("No Author")
        dateInfo = fileInfo[bestArticles[article]][5]
        try:
            print("Day is " + dateInfo[0], end=", ")
        except:
            pass
        try:
            print("Month is " + dateInfo[1], end=", ")
        except:
            pass
        try:
            print("Year is " + dateInfo[2])
        except:
            pass
        print()

wordList = ["double", "slit", "electron", "quantum"]
JSTORWordLookup(wordList,10)

