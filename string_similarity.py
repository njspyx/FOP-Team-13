import re
import nltk
stopwords = nltk.corpus.stopwords.words('english')

# print(stopwords)

def filterString(str):
    wordList = str.split()
    filtered_words = [word for word in wordList if word not in stopwords]
    return " ".join(x for x in filtered_words)

#str="For many years, children growing up in a single parent family have been viewed as different. Being raised by only one parent seems impossible to many yet over the decades it has become more prevalent. In today’s society many children have grown up to become emotionally stable and successful whether they had one or two parents to show them the rocky path that life bestows upon all human beings. The problem lies in the difference of children raised by single parents versus children raised by both a mother and a father. Does a child need both parents? Does a young boy need a father figure around? Does the government provide help for single parents? What role do step-parents and step-siblings play? With much speculation, this topic has become a very intriguin argument. What people must understand is that properly raising a child does not rely on the structure of a family but should be more focused on the process or values that are taught to these children as they learn to mature. Children of single parents can be just as progressive with emotional, social and behavioral skills as those with two parents. "
# print(filterString(str))

def splitPassage(str):
    return re.split('\. |\? |\! ', str)


# print(splitPassage(filterString(str)))