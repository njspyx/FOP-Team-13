import csv
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from io import StringIO
import re
from tqdm import tqdm
import json

jstorDir = "JSTOR Database" # must download this directory

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
            title = bookTitle(fullPath)
            abstract = bookAbstract(fullPath)
            author = bookAuthor(fullPath)
            url = bookURL(fullPath)
            date = bookDate(fullPath)

        elif fileName.startswith("journal"):
            title = journalTitle(fullPath)
            abstract = journalAbstract(fullPath)
            author = journalAuthor(fullPath)
            url = journalURL(fullPath)
            date = journalDate(fullPath)

        elif fileName.startswith("research"):
            title = researchTitle(fullPath)
            abstract = researchAbstract(fullPath)
            author = researchAuthor(fullPath)
            url = researchURL(fullPath)
            date = researchDate(fullPath)

        fileInfo.append((fileName, title, url, abstract, author, date))

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

def bookTitle(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")
        titleGroup = meta[0].findall("book-title-group")
        title = titleGroup[0].findall("book-title")
        return title[0].text
    except IndexError:
        return None

def journalTitle(path):
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

def researchTitle(path):
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

def bookAuthor(path):
    names = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        contrib = meta.findall("contrib-group")[0]
        for author in contrib.iter("contrib"):
            name = author.findall("name")[0]
            front = name.findall("given-names")[0].text
            sur = name.findall("surname")[0].text
            names.append(front + " " + sur)
        return names
    except:
        return None

def journalAuthor(path):
    names = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        front = root.findall("front")[0]
        meta = front.findall("article-meta")[0]
        contrib = meta.findall("contrib-group")[0]
        for author in contrib.iter("contrib"):
            name = author.findall("string-name")[0]
            front = name.findall("given-names")[0].text
            sur = name.findall("surname")[0].text
            names.append(front + " " + sur)
        return names
    except:
        return None

def researchAuthor(path):
    names = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        contrib = meta.findall("contrib-group")[0]
        for author in contrib.iter("contrib"):
            name = author.findall("name")[0]
            front = name.findall("given-names")[0].text
            sur = name.findall("surname")[0].text
            names.append(front + " " + sur)
        return names
    except:
        return None

def bookURL(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        uri = meta.findall("self-uri")[0]
        return list(uri.attrib.values())[0]

    except IndexError:
        return None


def journalURL(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        front = root.findall("front")[0]
        meta = front.findall("article-meta")[0]
        uri = meta.findall("self-uri")[0]
        return list(uri.attrib.values())[0]

    except IndexError:
        return None

def researchURL(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        uri = meta.findall("self-uri")[0]
        return list(uri.attrib.values())[0]

    except IndexError:
        return None

def bookDate(path): # order is day month year
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        pubDate = meta.findall("pub-date")[0]
        try:
            day = pubDate.find("day").text
        except:
            day = None
        try:
            month = pubDate.find("month").text
        except:
            month = None
        try:
            year = pubDate.find("year").text
        except:
            year = None
        return [day, month, year]

    except IndexError:
        return None

def journalDate(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        front = root.findall("front")[0]
        meta = front.findall("article-meta")[0]
        pubDate = meta.findall("pub-date")[0]
        try:
            day = pubDate.find("day").text
        except:
            day = None
        try:
            month = pubDate.find("month").text
        except:
            month = None
        try:
            year = pubDate.find("year").text
        except:
            year = None
        return [day, month, year]
    except IndexError:
        return None


def researchDate(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        meta = root.findall("book-meta")[0]
        pubDate = meta.findall("pub-date")[0]
        try:
            day = pubDate.find("day").text
        except:
            day = None
        try:
            month = pubDate.find("month").text
        except:
            month = None
        try:
            year = pubDate.find("year").text
        except:
            year = None
        return [day, month, year]

    except IndexError:
        return None


indexJSTORFiles(jstorDir)
