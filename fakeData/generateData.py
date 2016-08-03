# -*- coding: utf-8 -*-
# @Author: t-yubai
# @Date:   2016-07-21 13:26:31
# @Last Modified by:   t-yubai
# @Last Modified time: 2016-07-22 13:59:00

import spellRule
import csv
import os

class genFakeWordPair:
    def __init__(self):
        self.caseIssue = {}
        self.missingIssue = {}
        self.spellIssue = {}
        self.definitons = []

        self.spellIssueRule = spellRule.spellRule()

    def readFile(self, filename):
        with open(filename, 'rt') as f:
            for name in f:
                self.definitons.append(name[:-1])

    def readWord(self, word):
        self.definitons.append(word)

    def isLowCase(self, Char):
        return Char.islower()

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
                        wordSeg.append(seg)
                    abbreviation = ""
                    while i < wordLen and self.isLowCase(word[i]) is False:
                        abbreviation += word[i]
                        i += 1
                    wordSeg.append(abbreviation)
                    lo = i
                    continue
                else:
                    if (i == 0):
                        i += 1
                        continue
                    seg = word[lo:i]
                    wordSeg.append(seg)
                    lo = i
                    i += 1
            else:
                i += 1
        if lo < wordLen:
            wordSeg.append(word[lo:])
        return wordSeg

    def genCaseIssue(self):
        self.caseIssue = {}
        for word in self.definitons:
            wordSeg = self.genWordSeg(word)
            if len(wordSeg) <= 1:
                continue
            else:
                word0 = wordSeg[0]

                if len(word0) == 0:
                    return
                if self.isLowCase(word0[0]):
                    word0 = word0[0].upper() + word0[1:]
                tmpword = []
                self.caseIssue[word] = []
                self.__genCaseIssue(wordSeg, tmpword, word, 0)

    def __genCaseIssue(self, wordSeg, tmpword, word, idx):
        if len(tmpword) == len(wordSeg):
            data = ""
            for part in tmpword:
                data += part
            self.caseIssue[word].append(data)
            return
        for i in range(idx, len(wordSeg)):
            if(len(wordSeg[i]) == 0):
                continue
            tmpword.append(wordSeg[i])
            self.__genCaseIssue(wordSeg, tmpword, word, i + 1)
            tmpword.pop()
            wordSeg[i] = wordSeg[i][0].lower() + wordSeg[i][1:]
            tmpword.append(wordSeg[i])
            self.__genCaseIssue(wordSeg, tmpword, word, i + 1)
            tmpword.pop()

    def genMissingIssue(self):
        self.missingIssue = {}
        for word in self.definitons:
            wordSeg = self.genWordSeg(word)
            self.missingIssue[word] = []
            for i in range(0, len(wordSeg)):
                name = ""
                for j in range(0, len(wordSeg)):
                    if (j == i):
                        continue
                    else:
                        name = name + wordSeg[j]
                self.missingIssue[word].append(name)

    def __genSpellIssue(self, wrongSpellDic, tmpword, word, idx):
        if idx == len(wrongSpellDic):
            data = ""
            for part in tmpword:
                data += part
            self.spellIssue[word].append(data)
            return
        for i in range(0, len(wrongSpellDic[idx])):
            tmpword.append(wrongSpellDic[idx][i])
            self.__genSpellIssue(wrongSpellDic, tmpword, word, idx + 1)
            tmpword.pop()

    def genSpellIssue(self):
        self.spellIssue = {}
        for word in self.definitons:
            wordSeg = self.genWordSeg(word)

            wrongSpellDic = []
            for i in range(0, len(wordSeg)):
                wrongSpellItem = self.genWrongSpell(wordSeg[i])
                wrongSpellDic.append(wrongSpellItem)
            tmpword = []
            self.spellIssue[word] = []
            self.__genSpellIssue(wrongSpellDic, tmpword, word, 0)

    def genWrongSpell(self, seg):
        wrongSpellList = []
        for funName in self.spellIssueRule.fmap:
            wrongSpellList.extend(self.spellIssueRule.fmap[funName](seg))
        return wrongSpellList


    def writeToFile(self):
        try:
            os.mkdir("genData")
        except OSError:
            print "genData dir exsists\n"
        with open('./genData/caseIssue.csv', 'wb') as f:
            write = csv.writer(f)
            for key in self.caseIssue.keys():
                line = []
                line.append(key)
                line.extend(self.caseIssue[key])
                write.writerow(line)

        with open('./genData/missingIssue.csv', 'wb') as f:
            write = csv.writer(f)
            for key in self.missingIssue.keys():
                line = []
                line.append(key)
                line.extend(self.missingIssue[key])
                write.writerow(line)
        with open('./genData/spellIssue.csv', 'wb') as f:
            write = csv.writer(f)
            for key in self.spellIssue.keys():
                line = []
                line.append(key)
                line.extend(self.spellIssue[key])
                write.writerow(line)

    def genAndWrite(self):
        self.genMissingIssue()
        self.genCaseIssue()
        self.genSpellIssue()
        self.writeToFile()


