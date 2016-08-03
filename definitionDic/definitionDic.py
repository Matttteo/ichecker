'''
TODO
1. Early stop
2. Use [this](https://github.com/wolfgarbe/symspell) algorithm to speed up
3. Redefine distance
'''

import  collections
from spellcorrect import  spellCorrector
from fakeData import  spellRule

class varDictionary():
    def __init__(self):
        self.wordSegDic = {}
        self.candidateWordDic = collections.defaultdict(list)
        self.pos = 0
        self.wordDic = {}
        self.commonMistakes = {}
        self.spellCorrector = spellCorrector()
        self.wrongSpellRef = spellRule()

    def  addWord2(self, word):
        wordSeg = self.genWordSeg(word)
        fullIDList = []
        for seg in wordSeg:
            if seg  not in self.wordSegDic:
                self.wordSegDic[seg.lower()] = self.pos
                fullIDList.append(self.pos)
                self.pos += 1
            else:
                fullIDList.append(self.wordSegDic[seg.lower()])
        fullID = tuple(fullIDList)
        self.candidateWordDic[fullID].append(word)

        segLen = len(wordSeg)


        for i in range(2, segLen):
            for j in range(0, segLen - i + 1):
                fullIDList = []
                for  k in range(0, j):
                    fullIDList.append(self.wordSegDic[wordSeg[k].lower()])
                combineSeg = ''
                for l in range(j, j + i):
                    combineSeg += wordSeg[l].lower()
                if combineSeg not in self.wordSegDic:
                    self.wordSegDic[combineSeg] = self.pos
                    fullIDList.append(self.pos)
                    self.pos += 1
                else:
                    fullIDList.append(self.pos)
                for m in range(j + i, segLen):
                    fullIDList.append(self.wordSegDic[wordSeg[m].lower()])
                fullID = tuple(fullIDList)
                self.candidateWordDic[fullID].append(word)

    def isLowCase(self, Char):
        return Char.islower()

    def addWord(self, word):
        wordSeg = self.genWordSeg(word)
        self.genWordDic(wordSeg, word)
        misTakes = self.genCommonMistakes(wordSeg)


        for seg in wordSeg:
            self.spellCorrector.create_dictionary_entry(seg)
        segLen = len(wordSeg)


        for i in range(2, segLen+1):
            for j in range(0, segLen - i + 1):
                combineSeg = ''
                for l in range(j, j + i):
                    combineSeg += wordSeg[l]
                self.spellCorrector.create_dictionary_entry(combineSeg)

    def genCommonMistakes(self, wordSeg):
        misTakes = []
        for seg in wordSeg:
            misTakes.append(self.wrongSpellRef.genIssueWord(seg))
        return misTakes


    def genWordDic(self, wordSeg, word):
        wordTmp = ''
        for seg in wordSeg:
            wordTmp += seg
        self.wordDic[wordTmp] = word
        split = [(wordSeg[0:i], wordSeg[i:]) for i in range(len(wordSeg) + 1)]
        deletes = [a + b[1:] for a ,b in split if b]
        for d in deletes:
            wordTmp = ''
            for w in d:
                wordTmp += w
            self.wordDic[wordTmp] = word

    def query(self, word):
        wordSeg = self.genWordSeg(word)
        queryResult = []
        for i in range(len(wordSeg)):
            queryResult.append(self.spellCorrector.get_suggestions(wordSeg[i]))


        combineResult = self.combineHelper(queryResult)

        varItems = set([self.wordDic[cr] for cr in combineResult if cr in self.wordDic])
        return list(varItems)

    def __combineHelper(self, wordList, wordTemp, combineResult, idx, n):
        if(idx == n):
            result =''
            for seg in wordTemp:
                result += seg
            combineResult.append(result)
            return
        for i in range(len(wordList[idx])):
            wordTemp.append(wordList[idx][i][0])
            self.__combineHelper(wordList, wordTemp, combineResult, idx+1, n)
            wordTemp.pop()

    def combineHelper(self, wordList):
        n = len(wordList)
        wordTemp = []
        combineResult = []
        self.__combineHelper(wordList, wordTemp, combineResult, 0, n)
        return combineResult



    def test(self):
        self.readFile('D:\inconsistentCheck\definitonDic\definitions.txt')
        while True:
            word = raw_input("Enter a var name")
            if len(word) == 0:
                break
            varItems = self.query(word)
            print varItems



    def genWordSeg(self, word):

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

    def readFile(self, filename):
        with open(filename, 'rt') as f:
            for word in f:
                self.addWord(word[:-1])

vd = varDictionary()
vd.test()