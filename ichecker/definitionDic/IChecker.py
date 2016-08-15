
from spellcorrect2 import spellCorrector
from context import fakeData
from fakeData.spellRule import spellRule

import copy
import os

class checker():
    def __init__(self):
        self.spellCorrector = spellCorrector()
        self.nameReference = nameReference()
        self.segReference = segReference()
        self.segTool = segmentTool()
        self.combineTool = combineDifferentList()
        self.rawNames = set()

    def addName(self, name):
        self.rawNames.add(name)
        nameSeg = self.segTool.segName(name)
        self.nameReference.addName(nameSeg, name)

        for seg in nameSeg:
            self.segReference.addSeg(seg)

        segLen = len(nameSeg)
        for i in range(1, segLen+1):
            for j in range(0, segLen - i + 1):
                self.segReference.addSeg(''.join(nameSeg[j:j+i]))
                self.spellCorrector.create_dictionary_entry(''.join(nameSeg[j:j+i]))
                #print ''.join(nameSeg[j:j+i])
                self.segReference.addSeg(''.join(nameSeg[0:j]) + ''.join(nameSeg[j+i:]))
                self.spellCorrector.create_dictionary_entry(''.join(nameSeg[0:j]) + ''.join(nameSeg[j+i:]))
                #print ''.join(nameSeg[0:j]) + ''.join(nameSeg[j+i:])
                #self.segReference.addSeg(''.join(nameSeg[0:j]))
                #self.spellCorrector.create_dictionary_entry(''.join(nameSeg[0:j]))
                #self.segReference.addSeg(''.join(nameSeg[j+i:]))
                #self.spellCorrector.create_dictionary_entry(''.join(nameSeg[j+i:]))
        #for referencedSeg in self.segReference:
        #    self.spellCorrector.create_dictionary_entry(referencedSeg)


    def helper(self, segList,allResultList):
        queryResult = []
        Len = len(segList)
        for i in range(Len):
            #print segList[i]
            suggestions = self.spellCorrector.get_suggestions(segList[i])
            if len(suggestions) == 0:
                return
                    
            suggestions = [list(self.segReference.findReferenceSeg(suggestion))
                                for suggestion in suggestions
                                if self.segReference.findReferenceSeg(suggestion) != '']
            suggestions = set(self.segTool.flattenList(suggestions))
            #print suggestions
            queryResult.append(list(suggestions))
        possibleName = self.combineTool.combine(queryResult)
        #print possibleName
        resultList = [list(self.nameReference.findReferenceName(''.join(name))) for name in possibleName
                        if self.nameReference.findReferenceName(''.join(name)) != '']
        resultList = self.segTool.flattenList(resultList)
        allResultList.append(resultList)

    def query(self, queryName):
        querySeg = self.segTool.segName(queryName)
        #print querySeg
        segLen = len(querySeg)
        connectedLists = [querySeg]
        #building...
        allResultList = []
        for i in range(2, segLen+1):
            for j in range(0, segLen - i + 1):
                tmpList = querySeg[:j] + [(''.join(querySeg[j:j+i]))] + querySeg[j+i:]
                connectedLists.append(tmpList)
        for segList in connectedLists:
            #print segList
            self.helper(segList, allResultList)
        
        unorderedResultSet = set([])
        orderedResultList = []
        for resultList in allResultList:
            for result in resultList:
                if not unorderedResultSet.issuperset([result]):
                    orderedResultList.append(result)
                    unorderedResultSet.add(result)

        if len(orderedResultList) == 0:
            res = []
            minDistance = 100
            for rawname in self.rawNames:
                distance = self.spellCorrector.dameraulevenshtein(queryName, rawname) 
                if distance < minDistance:
                    minDistance = distance
                    res = [rawname]
                elif distance == minDistance:
                    res.append(rawname)
            return res
        return orderedResultList
                    
        ###
        # print querySeg
        # queryResult = []

        # segLen = len(querySeg)

        # for i in range(segLen):
        #     suggestions = self.spellCorrector.get_suggestions(querySeg[i])
        #     suggestions = set([self.segReference.findReferenceSeg(suggestion)
        #                        for suggestion in suggestions
        #                        if self.segReference.findReferenceSeg(suggestion) != ''])
        #     queryResult.append(list(suggestions))

        # possibleName = self.combineTool.combine(queryResult)
        # return [self.nameReference.findReferenceName(''.join(name)) for name in possibleName
        #         if self.nameReference.findReferenceName(''.join(name)) != '']

    def readFile(self, fileName):
        with open(fileName, 'rt') as f:
            for line in f:
                self.rawNames.add(line[:-1])
                self.addName(line[:-1])

    def test(self):
        self.readFile(os.path.abspath(os.path.join(os.path.dirname(__file__) + '..\..')) + r'\test\data\definitions.txt')
        #self.readFile(r'C:\Users\t-yubai\Desktop\definitions.txt')
        while True:
            name = raw_input("Enter a var name (q to quit) : \n")
            if len(name) == 0  or name == 'q':
                break
            varItems = self.query(name)
            print varItems


class nameReference():
    def __init__(self):
        self.referenceTable = {}

    def addName(self, nameSeg, name):
        #test
        if ''.join(nameSeg) not in self.referenceTable:
            self.referenceTable[''.join(nameSeg)] = set([name])
        else:
            self.referenceTable[''.join(nameSeg)].add(name)
        splits = [(nameSeg[0:i], nameSeg[i:]) for i in range(len(nameSeg) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        for d in deletes:
            if ''.join(d):
                #print ''.join(d)
                if ''.join(d) not in self.referenceTable:
                    self.referenceTable[''.join(d)] = set([name])
                else:
                    self.referenceTable[''.join(d)].add(name)

    def findReferenceName(self, queryName):
        if queryName in self.referenceTable:
            return self.referenceTable[queryName]
        else:
            return set()

    def findAllReferenced(self, name):
        result = []
        for item in self.referenceTable:
            if name in self.referenceTable[item]:
                result.append(item)
        return result

    def test(self):
        nameSeg = ['what', 'the', 'fuck']
        self.addName(nameSeg, 'WhatTheFuck')
        print [item for item in self.findAllReferenced('WhatTheFuck')]

class segReference():
    def __init__(self):
        self.referenceTable = {}
        self.wrongSpellRule = spellRule()

    def __iter__(self):
        return iter(self.referenceTable)

    def addSeg(self, seg):
        if seg  not in  self.referenceTable:
            self.referenceTable[seg] = set([seg])
        else:
            self.referenceTable[seg].add(seg)
        for wrongSpellSeg in self.wrongSpellRule.genIssueWord(seg):
            if wrongSpellSeg not in self.referenceTable:
                if wrongSpellSeg not in self.referenceTable:
                    self.referenceTable[wrongSpellSeg] = set([seg])
                else:
                     self.referenceTable[wrongSpellSeg].add(seg)

    def findReferenceSeg(self, querySeg):
        if querySeg in self.referenceTable:
            return  self.referenceTable[querySeg]
        else:
            return ''

    def findAllReferenced(self, seg):
        result = []
        for item in self.referenceTable:
            if seg in self.referenceTable[item]:
                result.append(item)
        return result

    def test(self):
        self.addSeg('token')
        self.addSeg('capacity')
        print [referenced for referenced in self.findAllReferenced('token')]
        print [referenced for referenced in self.findAllReferenced('capacity')]


class segmentTool():
    def __init__(self):
        pass

    def isLowCase(self, Char):
        return  Char.islower()

    def flattenList(self, wordList):
        ''' Given a list which may contain other list, return a flatten list contains all the elements

        For example:
        flattenWord([1,[2,3],[[4],[5],[6,7]]]) == [1,2,3,4,5,6,7]
        '''
        res = []
        if len(wordList) == 0:
            return res
        for elem in wordList:
            if type(elem) == list:
                elem = self.flattenList(elem)
                res.extend(elem)
            else:
                res.append(elem)
        return res

    def splitName(self, name):
        '''Given a name which may contain ' ' or '_', split it by these symbol and return a list

        For example:
        splitName('This is a_good_example  ') = ['This', 'is', 'a', 'good', 'example']

        '''
        res = [str.split('_') for str in name.split(' ')]
        res = [str for str in res if str]
        flattenRes = [res for res in self.flattenList(res)]
        return flattenRes

    def case(self, Char):
        if Char.isupper():
            return 1
        else:
            return 2

    def segWord(self, word):
        wordSeg = []
        wordLen = len(word)

        if wordLen == 0:
            return wordSeg
        
        i = 0
        tmp = ''
        while i < wordLen:
            tmp += word[i]
            if i == wordLen - 1 or self.case(word[i]) != self.case(word[i+1]):
                if i == wordLen - 1:
                    wordSeg.append(tmp)
                    return wordSeg
                if word[i].isupper():
                    if len(tmp) > 1:
                        wordSeg.append(tmp[:-1])                    
                    tmp = word[i]
                    i += 1
                else:
                    wordSeg.append(tmp)
                    tmp = ''
                    i += 1
            else:
                i += 1
        return wordSeg


    def segName(self, name):
        wordList = self.splitName(name)
        nameSeg = []
        for w in wordList:
            wordSeg = self.segWord(w)
            nameSeg.extend(wordSeg)
        nameSeg = [seg.lower() for seg in nameSeg]
        return nameSeg


    def test(self):
        while True:
            name = raw_input('enter a name')
            print self.segName(name)

class combineDifferentList():

    def combine(self, allList):
        listSize = len(allList)
        if listSize == 0:
            return []

        combineResult = []
        combineTemp = []
        self.__combine(combineResult, combineTemp, allList, 0, listSize)
        return combineResult

    def __combine(self, combineResult, combineTemp, allList, idx, listSize):
        if idx == listSize:
            combineResult.append(copy.deepcopy(combineTemp))
            return
        curList = allList[idx]
        curListSize = len(curList)
        if curListSize == 0:
            self.__combine(combineResult, combineTemp, allList, idx+1, listSize)
        for i in range(curListSize):
            combineTemp.append(curList[i])
            self.__combine(combineResult, combineTemp, allList, idx + 1, listSize)
            combineTemp.pop()

    def test(self):
        lista = ['a', 'b', 'c']
        listb = []
        listc = ['e', 'f', 'g']
        result = self.combine([lista, listb, listc])
        print result