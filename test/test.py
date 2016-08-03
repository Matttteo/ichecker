

def testAll():
    from context import definitonDic as dic
    combine = dic.IChecker.combinationDifferentList()
    combine.test()

    segTool = dic.IChecker.segmentWord()
    segTool.test()

    segRef = dic.IChecker.segReference()
    segRef.test()

    wordRef = dic.IChecker.wordReference()
    wordRef.test()

    checker = dic.checker()
    #checker = dic.IChecker.icheker()
    checker.test()
    
def testIchecker():
    from context import definitonDic
    ck = definitonDic.checker()
    ck.readFile('definitions.txt')
    while True:
        word = raw_input("Enter a var name(q to quit)")
        if len(word) == 0 or word == 'q':
            break
        varItems = ck.query(word)
        print varItems