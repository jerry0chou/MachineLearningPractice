import numpy as np


def change(Label):
    if Label == 'largeDoses':
        return 2
    elif Label=='smallDoses':
        return 1
    else:
        return 0

fr = open('datingTestSet3.txt')
arrayOLines = fr.readlines()
AllList = []
for line in arrayOLines:
    line = line.strip()
    lineList = line.split('\t')
    lineList[-1]=str(change(lineList[-1]))
    AllList.append(lineList)

print AllList

fp = open("test.txt",'wb')
for al in AllList:
    for a in al:
        fp.write(a)
        fp.write('\t')
    fp.write('\n')
fp.close()