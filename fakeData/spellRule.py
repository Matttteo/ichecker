import random
import string


class spellRule(object):
    """This class is used to add some wrong spell rules"""

    def __init__(self):
        super(spellRule, self).__init__()
        self.fmap = {
            'ly': self.lyIssue,
            'doubleToSingle': self.doubleToSingleIssue,
            #'missing': self.missingCharIssue,
            'surplus': self.surplusIssue,
            #'random': self.randomIssue,
            'ed' : self.edIssue,
        }
    def lyIssue(self, seg):
        res = []
        if (seg[-2:] != 'ly' and seg[-2:] != 'ty'):
            return res
        else:
            newSeg = seg[:-1] + 'ies'
            res.append(newSeg)
            return res

    def doubleToSingleIssue(self, seg):
        res = []
        Len = len(seg)
        pos = []
        for i in xrange(0, Len):
            if (i < Len - 1 and seg[i + 1] == seg[i]):
                pos.append(i)
        for p in pos:
            newSeg = seg[:p] + seg[p + 1:]
            res.append(newSeg)
        return res

    def missingCharIssue(self, seg):
        Len = len(seg)
        res = []
        for i in range(0, Len):
            p = random.randint(0, Len - 1)
            newSeg = seg[:p] + seg[p + 1:]
            res.append(newSeg)
        return res

    def surplusIssue(self, seg):
        Len = len(seg)
        res = []

        for i in range(0, Len):
            p = random.randint(0, Len - 1)
            newSeg = seg[:p] + seg[p] + seg[p + 1:]
            res.append(newSeg)
        return res

    def randomIssue(self, seg):
        Len = len(seg)
        res = []

        for i in range(0, Len):
            p = random.randint(0, Len - 1)
            c = random.choice(string.ascii_lowercase)
            newSeg = seg[:p] + c + seg[p + 1:]
            res.append(newSeg)
        return res

    def edIssue(self, seg):
        Len = len(seg)
        res = []
        if seg[-2:] == 'ed':
            newSeg = seg[:-2]
            res.append(newSeg)

        else:
            newSeg = seg + 'ed'
            res.append(newSeg)
        return res

    def addRule(self, fun, name):
        self.fmap[name] = fun

    def genIssueWord(self,word):
        res = []
        for fname in self.fmap:
            res.extend(self.fmap[fname](word))
        return set(res)




