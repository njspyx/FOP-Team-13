import en_core_web_sm
import warnings
import spacy
from spacy import tokenizer
from main.string_similarity import filterString
from main.string_similarity import splitPassage
import string
import heapq

warnings.filterwarnings('ignore')  # ignore warnings from jupyter notebooks/spacy
nlp = en_core_web_sm.load()  # load spacy library
#tokenizer = nlp.Defaults.create_tokenizer(nlp)

def getWordScores(str, repeatWeight, keyWords, keyWordWeight):
    str = str.lower()
    doc = nlp(str)

    scoreDic = {}
    for token in doc:
        keyWordFlag = False
        for keyWord in keyWords:
            if token.text in keyWord:
                scoreDic[token.text.strip()] = keyWordWeight
                keyWordFlag = True
                break
        if keyWordFlag:
            continue
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            scoreDic[token.text.strip()] = scoreDic.get(token.text.strip(), 0) + repeatWeight
        else:
            scoreDic[token.text.strip()] = 0
    return scoreDic


def updateWordScores(scoreDic, usedSentence, usedScore):
    for word in usedSentence.split(" "):
        try:
            if scoreDic[word.lower().strip()] > 0:
                scoreDic[word.lower().strip()] = scoreDic[word.lower().strip()] - usedScore
        except KeyError:
            continue
    return scoreDic

def sentenceScore(sentence, scoreDic):
    score = 0
    words = sentence.split()
    averaging = 0
    for word in words:
        try:
            if scoreDic[word.lower().strip()] != 0:
                averaging += 1
                score += scoreDic.get(word.lower().strip(), 0)
        except KeyError:
            continue

    if averaging==0:
        return 0
    return score/averaging

#repeatWeight should be positive, usedWeight should be negative
def summarizeText(inputStr, numSentences, repeatWeight, usedWeight, keyWords, keyWordWeight, bulletBool):
    
    startingSentenceList = splitPassage(inputStr)
    inputStr = filterString(inputStr)
    sentenceList = splitPassage(inputStr)

    scoreDic = getWordScores(inputStr, repeatWeight, keyWords, keyWordWeight)

    finishedIndices = []

    for iter in range(numSentences):
        maxScore = 0
        maxIndex = 0
        for s in range(len(sentenceList)):
            if s in finishedIndices: # prevents repetition
                continue
            sentence = sentenceList[s]
            score = sentenceScore(sentence, scoreDic)
            if score > maxScore:
                maxScore = score
                maxIndex = s
        finishedIndices.append(maxIndex)
        scoreDic = updateWordScores(scoreDic, sentenceList[maxIndex], usedWeight)

    finishedIndices.sort()
    finishedSentences = []

    for index in finishedIndices:
        if bulletBool:
            finishedSentences.append(sentenceList[index])
        else:
            finishedSentences.append(startingSentenceList[index])

    # get top words
    n = int(numSentences*1.5) + 1
    topList = heapq.nlargest(n, scoreDic, key=scoreDic.get)

    return finishedSentences, topList
 
    #finishedSentences contains the most important sentences but not sorted: we should probably sort them somehow


# string1 = "Bataille uses theterm 'textual nihilism' to denote the bridge between sexual identity andnarrativity.In a sense, Debord suggests the use of capitalist discourse to deconstructand modify class"
# print(splitPassage(string1))
# str1 = "For many years years years years, children growing up in a single parent family have been viewed as different. Being raised by only one parent seems impossible to many yet over the decades it has become more prevalent. In todayâ€™s society many children have grown up to become emotionally stable and successful whether they had one or two parents to show them the rocky path that life bestows upon all human beings. The problem lies in the difference of children raised by single parents versus children raised by both a mother and a father. Does a child need both parents? Does a young boy need a father figure around? Does the government provide help for single parents? What role do step-parents and step-siblings play? With much speculation, this topic has become a very intriguing argument. What people must understand is that properly raising a child does not rely on the structure of a family but should be more focused on the process or values that are taught to these children as they learn to mature. Children of single parents can be just as progressive with emotional, social and behavioral skills as those with two parents. "
# str2 = "The House of Representatives shall be composed of Members chosen every second Year by the People of the several States, and the Electors in each State shall have the Qualifications requisite for Electors of the most numerous Branch of the State Legislature. No Person shall be a Representative who shall not have attained to the Age of twenty five Years, and been seven Years a Citizen of the United States, and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen. Representatives and direct Taxes shall be apportioned among the several States which may be included within this Union, according to their respective Numbers, which shall be determined by adding to the whole Number of free Persons, including those bound to Service for a Term of Years, and excluding Indians not taxed, three fifths of all other Persons. The actual Enumeration shall be made within three Years after the first Meeting of the Congress of the United States, and within every subsequent Term of ten Years, in such Manner as they shall by Law direct. The Number of Representatives shall not exceed one for every thirty Thousand, but each State shall have at Least one Representative; and until such enumeration shall be made, the State of New Hampshire shall be entitled to chuse three, Massachusetts eight, Rhode-Island and Providence Plantations one, Connecticut five, New-York six, New Jersey four, Pennsylvania eight, Delaware one, Maryland six, Virginia ten, North Carolina five, South Carolina five, and Georgia three. When vacancies happen in the Representation from any State, the Executive Authority thereof shall issue Writs of Election to fill such Vacancies. The House of Representatives shall chuse their Speaker and other Officers; and shall have the sole Power of Impeachment."
# print(summarizeText(str1, 3, 5, -3))
# print(summarizeText(str2, 3, 5, -3))

if __name__ == "__main__":
    print("Start")
    with open("Sample Texts/communist.txt", "r", encoding="utf8") as f:
        keyWords = ["class", "proletariat"]
        summary = summarizeText(f.read(), 10, 1, -1, keyWords, 100, False)
        # summarizeText(inputStr, numSentences, repeatWeight, usedWeight, keyWords, keyWordWeight, bulletBool):
        with open("Summaries/communistsummary1.txt", "w", encoding="utf8") as g:
            for sentence in summary:
                g.write(sentence.replace('\n', '') + "\n")
                #g.write("\u2022 " + sentence + "\n")
    f.close()
    g.close()

    print("Done")