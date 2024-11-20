import numpy as np

def spatial(num_voters, candidates):

    num_candidates = len(candidates)

    voter_positions = np.random.rand(num_voters)
    candidate_positions = np.random.rand(num_candidates)
    
    voter_rankings = []
    
    for voter_pos in voter_positions:

        distances = np.abs(candidate_positions - voter_pos)
        ranking = [candidates[i] for i in np.argsort(distances)]
        voter_rankings.append(ranking)
    
    return voter_rankings