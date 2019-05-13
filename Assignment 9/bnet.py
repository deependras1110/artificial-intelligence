import sys
import copy

probability = {
    "B": 0.001,
    "E": 0.002,
    "A|B,E": 0.95,
    "A|B,nE": 0.94,
    "A|nB,E": 0.29,
    "A|nB,nE": 0.001,
    "J|A": 0.90,
    "J|nA": 0.05,
    "M|A": 0.70,
    "M|nA": 0.01
}

def getProbability(term):
    if term[0] == "n":
        return (1 - getProbability(term[1:]))
    if term in probability:
        return probability[term]

parents = {
    'A': ['B','E'], 
    'B': None, 
    'E': None, 
    'J': ['A'], 
    'M': ['A']
}
def findParents(array):
    newArray = []
    for node in array:
        newTerm = node + "|"
        if node[0] == "n":
            nodeParents = parents[node[1:]]
        else:
            nodeParents = parents[node]

        if nodeParents != None:
            for p in nodeParents:
                if p in array:
                    newTerm = newTerm + p + ","
                else:
                    newTerm = newTerm + "n" + p + ","
        
        newTerm = newTerm[0:len(newTerm)-1]
        newArray.append(newTerm)
    return newArray  

requiredTerms = ['A', 'B', 'E', 'J', 'M']
def computeProbability(array):
    if len(array) == 5:
        newArray = findParents(array)
        prod = 1
        for node in newArray:
            prod = prod * getProbability(node)
        return prod
    else:
        for missingNode in requiredTerms:
            if missingNode in array:
                continue
            else:
                flag = False
                for nodeArray in array:
                    if missingNode == nodeArray[1:]:
                        flag = True
                        break

                if flag == True:
                    continue
                else:
                    missedNode = missingNode
                    break

        normalArray = copy.deepcopy(array)
        negateArray = copy.deepcopy(array)
        normalArray.append(missedNode)
        negateArray.append("n"+missedNode)
        return computeProbability(normalArray) + computeProbability(negateArray)

def convertToProgramNotations(array):
    newArray = []
    for node in array:
        if node[1] == "t":
            newArray.append(node[0])
        else:
            newArray.append("n"+node[0])
    return newArray

def __main__(argv):
    if "given" in argv:
        givenIndex = argv.index("given")
        denominator = argv[givenIndex+1:]
        numerator = argv[1:givenIndex] + denominator
        n = computeProbability(convertToProgramNotations(numerator))
        d = computeProbability(convertToProgramNotations(denominator))
        print "Probability = " + str(n/d)
    else:
        print "Probability = " + str(computeProbability(convertToProgramNotations(argv[1:])))

__main__(sys.argv)