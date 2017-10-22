# -*- coding:utf-8 -*-
import math, operator
import os

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    # print '\nnumEntries=', numEntries
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    # print 'labelCounts', labelCounts
    for key in labelCounts:
        # print 'key=', key
        prob = float(labelCounts[key]) / numEntries
        # print 'prob=', prob
        shannonEnt -= prob * math.log(prob, 2)
        # print 'shannonEnt=', shannonEnt, '\n'
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        # print '\n', featVec, featVec[axis], value
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            # print 'red=',reducedFeatVec
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']
               ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        # print 'featList=',featList
        uniqueVals = set(featList)
        # print 'unique=',uniqueVals
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    '''
    :param classList: 
    :return: 
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    # print 'labels=',labels
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        # print 'subL=',subLabels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


def printDict(dict_a, result):
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            if isinstance(temp_value, dict):  # 将叶子节点全部加入
                for kk in temp_value:
                    temp_list = []
                    if isinstance(temp_value[kk], dict) == False:
                        temp_list.append(temp_key)
                        temp_list.append(kk)
                        temp_list.append(temp_value[kk])
                        result.append(temp_list)
                    elif isinstance(temp_value[kk], dict) and isinstance(temp_key,str ):
                        temp_list.append(temp_key)
                        temp_list.append(kk)
                        temp_list.append(temp_value[kk].keys()[0])
                        result.append(temp_list)
            printDict(temp_value, result)  # 自我调用实现无限遍历

def createDot(name, treeDict):
    file = open("tree.dot", 'wb')
    string = 'digraph ' + name + '{'
    result = []
    printDict(treeDict,result)
    print result
    string += '\n  node [shape="box" style = filled color=lightblue];\n'
    dotNames = []
    relation = ''
    for re in result:
        if re[0] not in dotNames:
            dotNames.append(re[0])
        dotNames.append(re[2])

    dotDict=dict(zip(range(len(dotNames)), dotNames))
    sign=list(range(len(dotNames)))
    for re in result:
        for key in dotDict:
            if re[0]==dotDict[key]:
                re[0]=key
            elif re[2]==dotDict[key] and key in sign:
                re[2]=key
                sign.remove(key)

    for a in range(len(dotNames)):
        string += '  ' + str(a) +' [label="%s"]'%str(dotDict[a]) + ';\n'

    for re in result:
        relation += '  ' + str(re[0]) + ' -> ' + str(re[2]) + ' [label="%s"]'%str(re[1])+ ';\n';

    string = string + relation
    string += '\n}'
    file.write(string)
    file.close()
    os.system('dot -Tpdf tree.dot -o tree.pdf')

myDat, labels = createDataSet()
# print myDat, calcShannonEnt(myDat)
# print myDat
# print splitDataSet(myDat,0,1)
# print chooseBestFeatureToSplit(myDat)
treeDict=createTree(myDat,labels)
#treeDict = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}, 2: {'maybe': {0: 'test'}}}}
createDot('g', treeDict)
