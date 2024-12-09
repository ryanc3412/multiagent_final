import numpy as np
from itertools import permutations

def spatial(num_voters, num_candidates):
    candidates=[i for i in range(num_candidates)]

    voter_positions = np.random.rand(num_voters)
    candidate_positions = np.random.rand(num_candidates)
    
    voter_rankings = []
    
    for voter_pos in voter_positions:

        distances = np.abs(candidate_positions - voter_pos)
        ranking = [candidates[i] for i in np.argsort(distances)]
        voter_rankings.append(tuple(ranking))
    
    #Convert the voter rankings to the same format as the other populations
    perms = list(permutations(candidates))
    permutation_count = [0 for i in range(len(perms))]
    for voter in voter_rankings:
        index = perms.index(voter)
        permutation_count[index] +=1
    result = [(perms[i], permutation_count[i]) for i in range(len(perms))]

    return result