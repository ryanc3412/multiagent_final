#!!!!!!!!!!!!!!!!!!!!RENAME LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def buildPrecedenceTable(num_candidates, population):
    precedes = [[0 for i in range(num_candidates)] for j in range(num_candidates)]
    for subPopulation in population:
        order = subPopulation[0]
        for i in range(num_candidates-1):
            for j in range(i+1, num_candidates):
                precedes[order[i]][order[j]] += subPopulation[1]
    return precedes
        
def getCopelandDeficiency(precedenceTable, num_candidates):
    copeScores = getCopelandScores(precedenceTable, num_candidates)
    maxScore = max(copeScores)
    return [x - maxScore for x in copeScores]      

def getCopelandScores(precedenceTable, num_candidates):
    scores = [0 for i in range(num_candidates)]
    for i in range(num_candidates):
        for j in range(num_candidates):
            if i==j:
                continue
            if precedenceTable[i][j] > precedenceTable[j][i]:
                scores[i] +=1
            else:
                scores[i] -=1
    return scores

#Takes a precedence table and returns the condorcet winner and loser.  If there is no winner/lower, -1 is returned instead
def getCondorcetWinnerLoser(precedenceTable, num_candidates):
    copeScores = getCopelandScores(precedenceTable, num_candidates)
    winner = -1
    loser = -1
    for i in range(num_candidates):
        # If a condorcet winner exists, its copeland score is equal to the number of candidates minus 1
        if copeScores[i] == num_candidates - 1:
            winner = i
        # If a condorcet loser exists, its copeland score is -(number of candidates -1), or 1 minus the number of candidates
        elif copeScores[i] == 1 - num_candidates:
            loser = i
    return winner, loser

def fullCondorcet(num_candidates, population):
    precTable = buildPrecedenceTable(num_candidates, population)
    copeScores = getCopelandScores(precTable, num_candidates)
    winner=-1
    loser=-1
    for i in range(num_candidates):
        # If a condorcet winner exists, its copeland score is equal to the number of candidates minus 1
        if copeScores[i] == num_candidates - 1:
            winner = i
        # If a condorcet loser exists, its copeland score is -(number of candidates -1), or 1 minus the number of candidates
        elif copeScores[i] == 1 - num_candidates:
            loser = i
    maxScore = max(copeScores)
    return winner, loser, [x - maxScore for x in copeScores]


