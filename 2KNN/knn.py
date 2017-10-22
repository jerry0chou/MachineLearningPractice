import numpy as np
import operator
import os
import matplotlib
import matplotlib.pyplot as plt


def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0.0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inx, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inx, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distance = sqDistances ** 0.5
    # print 'dataset',dataSet
    # print 'distance',distance
    sortedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # print 'sortedDistIndicies[%d]'%(i),sortedDistIndicies[i]
        # print 'voteIlabel',voteIlabel
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
        # print 'classCount[i]',classCount[voteIlabel]
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    # print 'classCount',classCount
    # print 'sortedClassCount',sortedClassCount
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    lines = len(arrayOLines)
    returnMat = np.zeros((lines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        lineList = line.split('\t')
        returnMat[index, :] = lineList[0:3]
        classLabelVector.append(int(lineList[-1]))
        index += 1
    print 'returnMat', returnMat
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    # print 'jerry',minVals,maxVals,ranges
    normDataSet = np.zeros(np.shape(dataSet))
    # print'normDateSet=' ,normDataSet
    m = dataSet.shape[0]
    # print'm=',m
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    # print 'np.tile(minVals,(m,1))=',np.tile(minVals, (m, 1))
    normDataSet = normDataSet / np.tile(ranges, (m, 1))
    # print 'np.tile(ranges, (m, 2))=', np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.1
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    print 'numTestVecs=', numTestVecs
    errorCount = 0.0
    for i in range(numTestVecs):
        classfierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], \
                                    datingLabels[numTestVecs:m], 3)
        print 'the classfier came back with:%d,the real answer is :%d' \
              % (classfierResult, datingLabels[i])
        if (classfierResult != datingLabels[i]): errorCount += 1.0
    print "errorCount=", errorCount
    print 'the total error rate is :%f' % (errorCount / float(numTestVecs))


def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input( \
        'percentage of time spend playing video games?'
    ))
    ffMiles = float(raw_input("frequent filter miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = np.array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print 'you will probably like this person :', resultList[classifierResult - 1]


def img2vector(filename):
    returnVect = np.zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])

    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = np.zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('digits/trainingDigits/%s' % fileNameStr)

    testFileList = os.listdir('digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('digits/testDigits/%s' %fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print 'the classifier came back with:%d,the real answer is :%d' % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print '\nthe total number of error is :%d' % errorCount
    print '\nthe total error rate is:%f' % (errorCount / float(mTest))


#handwritingClassTest()

# testVector=img2vector('digits/testDigits/0_13.txt')
# print testVector[0,32:63]

#datingClassTest()
classifyPerson()

# datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
# print datingDataMat, '\n', datingLabels[0:20]

# normMat, ranges, minVals = autoNorm(datingDataMat)
# print normMat, '\n', ranges, '\n', minVals

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(datingDataMat[:, 0], datingDataMat[:, 2])
# plt.show()
# g, l = createDataSet()
# print classify0(inx=[0, 0], dataSet=g, labels=l, k=3)
