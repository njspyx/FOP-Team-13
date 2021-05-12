from flask import Flask, jsonify, request
from main.nlp import summarizeText
from main.ocr import imageToText

import json
import time

with open("fileInfo.json", "r") as rfi:
    fileInfo = json.load(rfi)
with open("wordIndex.json", "r") as rwi:
    wordIndex = json.load(rwi)

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def get_ocr():
    img = request.files["image"]
    ocr_text = imageToText(img)
    return jsonify({"text" : ocr_text})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.form

    is_bullet = json.loads(data["bullets"].lower())
    keyword_list = data["keywords"].split(",")
    summary, top_words = summarizeText(data["text"], int(data["num_sentences"]), 1, -1, keyword_list, 10, is_bullet)

    result = ""
    for sentence in summary:
            if not is_bullet:
                result += sentence.replace('\n', '') + "\n"
            else:
                result += "\u2022 " + sentence + "\n"
    
    return jsonify({"text" : result, "top_words": " ".join(top_words)})

@app.route("/jstor", methods=["POST"])
def JSTORWordLookup(): #assumes they are already set
    data = request.form
    indexArrays = []
    frequencyChart = {}
    
    for word in data["words"].split(" "):
        if word in wordIndex:
            indexArrays.append(wordIndex[word])

    for list in indexArrays:
        for index in list:
            frequencyChart[index] = frequencyChart.get(index, 0) + 1

    results = []
    bestArticles = sorted(frequencyChart, key=frequencyChart.get, reverse=True)
    for i in range(int(data["num_articles"])):
        results.append({
            "title": str(fileInfo[bestArticles[i]][1]),
            "abstract": str(fileInfo[bestArticles[i]][2]),
        })
    return jsonify({"articles": results})


if __name__ == "__main__":
    app.run()

