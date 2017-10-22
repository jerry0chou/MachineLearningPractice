# -*- coding:utf-8 -*-
#from numpy import *
import numpy as np
import re
def loadDataSet():
    postingList=[['my','dog','has','flea',\
                  'problems','help','please'],
                 ['maybe','not','take','him',\
                  'to','dog','park','stupid'],
                 ['my','dalmation','is','so','cute',\
                  'I','love','him'],
                 ['stop','posting','stupid','worthless','garbage'],
                 ['mr','licks','ate','my','steak','how',\
                  'to','stop','him'],
                 ['quit','buying','worthless','dog','food','stupid']
    ]
    classVec=[0,1,0,1,0,1] # 1 代表侮辱性文字 0代表正常言论
    return postingList,classVec

def createVocabList(dataSet):
    '''
    :param dataSet: 词汇集
    :return: 不重复的单词集合列表
    '''
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print 'the word %s is not in my Vocabulary!'% word

    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)      #change to ones()
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = np.log(p1Num/p1Denom)          #change to log()
    p0Vect = np.log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive


def classifyNB(vec2Classify,p0vec,p1vec,pClass):
    p1=sum(vec2Classify*p1vec)+np.log(pClass)
    p0=sum(vec2Classify*p0vec)+np.log(1.0-pClass)
    if p1>p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses=loadDataSet()
    myVocabList=createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0v, p1v, pAb = trainNB0(np.array(trainMat),np.array(listClasses))
    testEntry=['love','my','dalmation']
    thisDoc=np.array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as :',classifyNB(thisDoc,p0v,p1v,pAb)
    testEntry=['stupid','garbage']
    thisDoc=np.array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as :',classifyNB(thisDoc,p0v,p1v,pAb)

def bagOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec

def textParse(bigString):
    listOfTokens=re.split(r'W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamTest():
    docList=[]
    classList=[]
    fullText=[]
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    trainingSet=range(50)
    testSet=[]
    for i in range(10):
        randIndex=int(np.random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[]
    trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0v,p1v,pSpam=trainNB0(np.array(trainMat),np.array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(np.array(wordVector),p0v,p1v,pSpam)!=classList[docIndex]:
            errorCount+=1
    print 'the error rate is：',float(errorCount)/len(testSet)



# listOPosts,listClasses=loadDataSet()
# myVocabList=createVocabList(listOPosts)
# print myVocabList
# print setOfWords2Vec(myVocabList,listOPosts[0])
# print setOfWords2Vec(myVocabList,listOPosts[3])

# trainMat=[]
# for postinDoc in listOPosts:
#     #print postinDoc
#     trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
#
# for tr in trainMat:
#     print tr
# print listClasses
# p0v,p1v,pAb=trainNB0(trainMat,listClasses)
# print pAb
# print p0v
# print p1v

#testingNB()

#mySent='This book is the best book on Python or M.L. I have ever laid eyes upon.'
#print mySent.split()
# import re
# regEx=re.compile('\\W*')
# listOfTokens=regEx.split(mySent)
# print listOfTokens
# print [tok for tok in listOfTokens if len(tok)>0]
# print [tok.lower() for tok in listOfTokens if len(tok)>0]

# emailText=open('email/ham/6.txt').read()
# listOfTokens=regEx.split(emailText)
# print listOfTokens

spamTest()