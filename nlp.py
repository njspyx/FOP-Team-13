import en_core_web_lg
import warnings
import spacy
from spacy import tokenizer
from string_similarity import filterString
from string_similarity import splitPassage
import string

warnings.filterwarnings('ignore')  # ignore warnings from jupyter notebooks/spacy
nlp = en_core_web_lg.load()  # load spacy library
#tokenizer = nlp.Defaults.create_tokenizer(nlp)

def wordTypeCheck(word):
    return (nlp(word)[0].pos_ == "PROPN" or nlp(word)[0].pos_ == "NOUN")

def getWordScores(str, repeatWeight):
    str = str.lower()
    for c in string.punctuation:
        str = str.replace(c, "")
    wordList = str.split(" ")
    scoreDic = {}
    for word in wordList:
        if wordTypeCheck(word):
            scoreDic[word] = scoreDic.get(word, 0) + repeatWeight
    return scoreDic

def updateWordScores(scoreDic, usedSentence, usedScore):
    for usedWord in usedSentence.split():
        if wordTypeCheck(usedWord):
            scoreDic[usedWord] = usedScore
    return scoreDic

def sentenceScore(sentence, scoreDic):
    score = 0
    words = sentence.split()
    averaging = 0
    for word in words:
        if wordTypeCheck(word):
            averaging += 1
            score += scoreDic.get(word, 0)
    return score/averaging

#repeatWeight should be positive, usedWeight should be negative
def summarizeText(str, numSentences, repeatWeight, usedWeight):
    str = filterString(str)
    sentenceList = splitPassage(str)

    scoreDic = getWordScores(str, repeatWeight)

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
    #finishedSentences contains the most important sentences but not sorted: we should probably sort them somehow



str1 = "For many years years years years, children growing up in a single parent family have been viewed as different. Being raised by only one parent seems impossible to many yet over the decades it has become more prevalent. In today’s society many children have grown up to become emotionally stable and successful whether they had one or two parents to show them the rocky path that life bestows upon all human beings. The problem lies in the difference of children raised by single parents versus children raised by both a mother and a father. Does a child need both parents? Does a young boy need a father figure around? Does the government provide help for single parents? What role do step-parents and step-siblings play? With much speculation, this topic has become a very intriguing argument. What people must understand is that properly raising a child does not rely on the structure of a family but should be more focused on the process or values that are taught to these children as they learn to mature. Children of single parents can be just as progressive with emotional, social and behavioral skills as those with two parents. "
str2 = "The House of Representatives shall be composed of Members chosen every second Year by the People of the several States, and the Electors in each State shall have the Qualifications requisite for Electors of the most numerous Branch of the State Legislature. No Person shall be a Representative who shall not have attained to the Age of twenty five Years, and been seven Years a Citizen of the United States, and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen. Representatives and direct Taxes shall be apportioned among the several States which may be included within this Union, according to their respective Numbers, which shall be determined by adding to the whole Number of free Persons, including those bound to Service for a Term of Years, and excluding Indians not taxed, three fifths of all other Persons. The actual Enumeration shall be made within three Years after the first Meeting of the Congress of the United States, and within every subsequent Term of ten Years, in such Manner as they shall by Law direct. The Number of Representatives shall not exceed one for every thirty Thousand, but each State shall have at Least one Representative; and until such enumeration shall be made, the State of New Hampshire shall be entitled to chuse three, Massachusetts eight, Rhode-Island and Providence Plantations one, Connecticut five, New-York six, New Jersey four, Pennsylvania eight, Delaware one, Maryland six, Virginia ten, North Carolina five, South Carolina five, and Georgia three. When vacancies happen in the Representation from any State, the Executive Authority thereof shall issue Writs of Election to fill such Vacancies. The House of Representatives shall chuse their Speaker and other Officers; and shall have the sole Power of Impeachment."
print(summarizeText(str1, 3, 5, -3))
print(summarizeText(str2, 3, 5, -3))