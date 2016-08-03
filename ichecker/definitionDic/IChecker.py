
from spellcorrect import spellCorrector
from context import fakeData
from fakeData.spellRule import spellRule

import copy
import os

class checker():
    '''
    This class is
    '''
    def __init__(self):
        self.spellCorrector = spellCorrector()
        self.wordReference = wordReference()
        self.segReference = segReference()
        self.segTool = segmentWord()
        self.combineTool = combinationDifferentList()

    def addWord(self, word):
        wordSeg = self.segTool.segWord(word)
        self.wordReference.addWord(wordSeg, word)

        for seg in wordSeg:
            self.segReference.addSeg(seg)

        segLen = len(wordSeg)
        for i in range(1, segLen+1):
            for j in range(0, segLen - i + 1):
                self.segReference.addSeg(''.join(wordSeg[j:j+i]))
                self.segReference.addSeg(''.join(wordSeg[0:j]).join(wordSeg[j+i:]))

        for referencedSeg in self.segReference:
            self.spellCorrector.create_dictionary_entry(referencedSeg)

    def query(self, queryWord):
        querySeg = self.segTool.segWord(queryWord)
        queryResult = []

        segLen = len(querySeg)

        for i in range(segLen):
            suggestions = self.spellCorrector.get_suggestions(querySeg[i])
            suggestions = set([self.segReference.findReferenceSeg(suggestion)
                               for suggestion in suggestions
                               if self.segReference.findReferenceSeg(suggestion) != ''])
            queryResult.append(list(suggestions))

        possibleWord = self.combineTool.combine(queryResult)
        return [self.wordReference.findReferenceWord(''.join(word)) for word in possibleWord
                if self.wordReference.findReferenceWord(''.join(word)) != '']

    def readFile(self, fileName):
        with open(fileName, 'rt') as f:
            for word in f:
                self.addWord(word[:-1])

    def test(self):
        self.readFile(os.path.abspath(os.path.join(os.path.dirname(__file__) + '..\..')) + r'\test\data\definitions.txt')
        #self.readFile(r'C:\Users\t-yubai\Desktop\definitions.txt')
        while True:
            word = raw_input("Enter a var name (q to quit) : \n")
            if len(word) == 0  or word == 'q':
                break
            varItems = self.query(word)
            print varItems


class wordReference():
    def __init__(self):
        self.referenceTable = {}

    def addWord(self, wordSeg, word):
        self.referenceTable[''.join(wordSeg)] = word
        splits = [(wordSeg[0:i], wordSeg[i:]) for i in range(len(wordSeg) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        for d in deletes:
            self.referenceTable[''.join(d)] = word

    def findReferenceWord(self, queryWord):
        if queryWord in self.referenceTable:
            return self.referenceTable[queryWord]
        else:
            return ''

    def findAllReferenced(self, word):
        result = []
        for item in self.referenceTable:
            if self.referenceTable[item] == word:
                result.append(item)
        return result

    def test(self):
        wordSeg = ['what', 'the', 'fuck']
        self.addWord(wordSeg, 'WhatTheFuck')
        print [item for item in self.findAllReferenced('WhatTheFuck')]

class segReference():
    def __init__(self):
        self.referenceTable = {}
        self.wrongSpellRule = spellRule()

    def __iter__(self):
        return iter(self.referenceTable)

    def addSeg(self, seg):
        self.referenceTable[seg] = seg
        for wrongSpellSeg in self.wrongSpellRule.genIssueWord(seg):
            if wrongSpellSeg not in self.referenceTable:
                self.referenceTable[wrongSpellSeg] = seg

    def findReferenceSeg(self, querySeg):
        if querySeg in self.referenceTable:
            return  self.referenceTable[querySeg]
        else:
            return ''

    def findAllReferenced(self, seg):
        result = []
        for item in self.referenceTable:
            if self.referenceTable[item] == seg:
                result.append(item)
        return result

    def test(self):
        self.addSeg('token')
        self.addSeg('capacity')
        print [referenced for referenced in self.findAllReferenced('token')]
        print [referenced for referenced in self.findAllReferenced('capacity')]

class segmentWord():
    def __init__(self):
        pass

    def isLowCase(self, Char):
        return  Char.islower()
    def segWord(self, word):
        '''
        TODO:
        The function now is very fragile, need more works
        :param word:
        :return:
        '''
        wordLen = len(word)
        wordSeg = []
        lo = 0
        i = 0
        while i < wordLen:
            if self.isLowCase(word[i]) is False:
                if i + 1 < wordLen and self.isLowCase(word[i + 1]) is False:
                    if i != 0:
                        seg = word[lo:i]
                        wordSeg.append(seg.lower())
                    abbreviation = ""
                    while i < wordLen and self.isLowCase(word[i]) is False:
                        abbreviation += word[i]
                        i += 1
                    wordSeg.append(abbreviation.lower())
                    lo = i
                    continue
                else:
                    if (i == 0):
                        i += 1
                        continue
                    seg = word[lo:i]
                    wordSeg.append(seg.lower())
                    lo = i
                    i += 1
            else:
                i += 1
        if lo < wordLen:
            wordSeg.append(word[lo:].lower())
        return wordSeg

    def test(self):
        print self.segWord("whatTheFuck")

class combinationDifferentList():

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