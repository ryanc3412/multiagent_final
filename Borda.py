CERVONE_CONSTANT = 1.42554

def generateBordaVector(type, candidates, power):
    if type=="linear":
        borda = [((candidates-i)/(candidates-1))**power for i in range(1, candidates+1)]
        return borda
    elif type=="inverse":
        borda = [((candidates-i)/(i*(candidates-1)))**power for i in range(1, candidates+1)]
        return borda
    else:
        return None