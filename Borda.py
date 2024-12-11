CERVONE_CONSTANT = 1.42554

def generateBordaVector(type, candidates, power):
    if type=="linear":
        bordaVector = [((candidates-i)/(candidates-1))**power for i in range(1, candidates+1)]
        return bordaVector
    elif type=="inverse":
        bordaVector = [((candidates-i)/(i*(candidates-1)))**power for i in range(1, candidates+1)]
        return bordaVector
    else:
        return None
    
def findBordaWinner(scoreVector, candidates, population):
    scores = [0] * candidates
    for scoreTuple in population:
        order = scoreTuple[0]
        groupSize = scoreTuple[1]
        for i in range(candidates):
            scores[order[i]] += scoreVector[i] * groupSize
    winner = max([j for j in range(candidates)], key=lambda k: scores[k])
    #print("The winner is:", winner)
    return winner