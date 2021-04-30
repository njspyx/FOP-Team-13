import csv
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from io import StringIO
import re
from tqdm import tqdm
import json

jstorDir = "C:\\Users\\phill\\Documents\\Blair 2020-2021\\Future of Programming\\Note Taking App\\JSTOR Database"

def filterLetters(str):
    return re.sub("[^a-zA-Z]+", "", str.lower())

def indexJSTORFiles(jstorDir):
    count = -1
    fileInfo = []
    wordIndex = {}

    for fileName in tqdm(os.listdir(jstorDir)):
        count += 1
        if not fileName.endswith(".xml"):
            continue

        fullPath = jstorDir+"\\"+fileName
        if fileName.startswith("book"):
            title = bookInfo(fullPath)
            abstract = bookAbstract(fullPath)
        elif fileName.startswith("journal"):
            title = journalInfo(fullPath)
            abstract = journalAbstract(fullPath)
        elif fileName.startswith("research"):
            title = researchInfo(fullPath)
            abstract = researchAbstract(fullPath)

        fileInfo.append((fileName, title, abstract))

        if title != None:
            for word in title.split(" "):
                formatWord = filterLetters(word)
                if formatWord in wordIndex:
                    if count not in wordIndex[formatWord]:
                        wordIndex[formatWord].append(count)
                else:
                    wordIndex[formatWord] = [count]

        if abstract != None:
            for word in abstract.split(" "):
                formatWord = filterLetters(word)
                if formatWord in wordIndex:
                    if count not in wordIndex[formatWord]:
                        wordIndex[formatWord].append(count)
                else:
                    wordIndex[formatWord] = [count]

    with open("fileInfo.json", "w") as fi:
        json.dump(fileInfo, fi)

    with open("wordIndex.json", "w") as wi:
        json.dump(wordIndex, wi)

def bookInfo(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")
        titleGroup = meta[0].findall("book-title-group")
        title = titleGroup[0].findall("book-title")
        return title[0].text
    except IndexError:
        return None

def journalInfo(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        front = root.findall("front")
        meta = front[0].findall("article-meta")
        titleGroup = meta[0].findall("title-group")
        title = titleGroup[0].findall("article-title")
        return title[0].text
    except IndexError:
        return None

def researchInfo(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")
        titleGroup = meta[0].findall("book-title-group")
        title = titleGroup[0].findall("book-title")
        return title[0].text
    except IndexError:
        return None

def bookAbstract(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        body = root.findall("body")[0][0]
        for part in body.iter("book-part"):
            if len(part[0].findall("abstract")) != 0:
                return part[0].findall("abstract")[0][0].text
        return None
    except IndexError:
        return None

def journalAbstract(path):
    try:
        abstract = ET.parse(path).getroot().findall("front")[0].findall("article-meta")[0].findall("abstract")
        return abstract[0][0].text
    except IndexError:
        return None

def researchAbstract(path):
    try:
        abstract = ET.parse(path).getroot().findall("book-meta")[0].findall("abstract")
        return abstract[0][0].text
    except IndexError:
        return None

indexJSTORFiles(jstorDir)

