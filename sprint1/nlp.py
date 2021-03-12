import en_core_web_sm
import spacy
import string
import nltk
import re

nlp = spacy.load('en_core_web_sm')  # load spacy library
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

def filterString(str):
    wordList = str.split()
    filteredWords = [word for word in wordList if word not in stopwords]
    return " ".join(filteredWords)
 
def splitPassage(str):
    return re.split('\. |\? |\! ', str)
  
def getWordScores(str, repeatWeight):
    str = str.lower()
    doc = nlp(str)

    scoreDic = {}
    for token in doc:
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            scoreDic[token.text] = scoreDic.get(token.text, 0) + repeatWeight
    return scoreDic
 
def updateWordScores(scoreDic, usedSentence, usedScore):
    for token in nlp(usedSentence):
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            scoreDic[token.text] = usedScore
    return scoreDic
 
def sentenceScore(sentence, scoreDic):
    score = 0
    words = sentence.split()
    averaging = 0
    for word in words:
        averaging += 1
        score += scoreDic.get(word, 0)

    if averaging:
      return score/averaging
    else:
      return 0

#repeatWeight should be positive, usedWeight should be negative
def summarizeText(inputStr, numSentences, repeatWeight, usedWeight):

    inputStr = filterString(inputStr)
    sentenceList = splitPassage(inputStr)
 
    scoreDic = getWordScores(inputStr, repeatWeight)
 
    finishedIndices = []
 
    for iter in range(numSentences):
        maxScore = 0
        maxIndex = 0
        for s in range(len(sentenceList)):
            sentence = sentenceList[s]
            if sentenceScore(sentence, scoreDic) > maxScore:
                maxScore = sentenceScore(sentence, scoreDic)
                maxIndex = s
        finishedIndices.append(maxIndex)
        scoreDic = updateWordScores(scoreDic, sentenceList[maxIndex], usedWeight)
        #should inherently avoid repeating words since every word would be negative
 
    finishedIndices.sort()
    finishedSentences = []
    for index in finishedIndices:
        finishedSentences.append(sentenceList[index])
 
    return finishedSentences


if __name__ == "__main__":
    str1 = "For many years years years years, children growing up in a single parent family have been viewed as different. Being raised by only one parent seems impossible to many yet over the decades it has become more prevalent. In today’s society many children have grown up to become emotionally stable and successful whether they had one or two parents to show them the rocky path that life bestows upon all human beings. The problem lies in the difference of children raised by single parents versus children raised by both a mother and a father. Does a child need both parents? Does a young boy need a father figure around? Does the government provide help for single parents? What role do step-parents and step-siblings play? With much speculation, this topic has become a very intriguing argument. What people must understand is that properly raising a child does not rely on the structure of a family but should be more focused on the process or values that are taught to these children as they learn to mature. Children of single parents can be just as progressive with emotional, social and behavioral skills as those with two parents. "
    str2 = "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defense, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."
    print(summarizeText(str1, 3, 5, -3))
    print(summarizeText(str2, 3, 5, -3))