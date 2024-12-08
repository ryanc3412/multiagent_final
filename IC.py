# impartial anonymous culture
import random
from itertools import permutations


def generate_ic_voters(num_voters, candidates):
    rankings = list(permutations([i for i in range(candidates)]))
    num_rankings = len(rankings)

    counts = [0] * num_rankings

    for _ in range(num_voters):
        chosen_index = random.choice(range(num_rankings))
        counts[chosen_index] += 1

    result = []
    for i in range(num_rankings):
        if counts[i] != 0:
            result.append((rankings[i], counts[i]))

    return result