

import random
from itertools import permutations


def generate_iac_voters(num_voters, candidates):
    rankings = list(permutations([i for i in range(candidates)]))
    num_rankings = len(rankings)

    votes = [0] * (num_rankings + 1)
    for i in range(1, num_rankings):
        votes[i] = random.randint(0, num_voters)
    votes[0] = 0
    votes[num_rankings] = num_voters
    votes.sort()

    result = []
    for i in range(num_rankings):
        result.append((rankings[i], votes[i+1]-votes[i]))

    return result