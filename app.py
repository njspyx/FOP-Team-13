from flask import Flask, jsonify, request
from main.nlp import summarizeText
from main.ocr import imageToText

import json

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
    summary = summarizeText(data["text"], int(data["num_sentences"]), 1, -1, keyword_list, 10, is_bullet)

    result = ""
    for sentence in summary:
            if not is_bullet:
                result += sentence.replace('\n', '') + "\n"
            else:
                result += "\u2022 " + sentence + "\n"
    
    return jsonify({"text" : result})


if __name__ == "__main__":
    app.run()
