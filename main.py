# Teancum, Jared, & Ryan
# 5110 Final project

from IAC import generate_iac_voters
from borda_dominance import calculate_borda_dominance

# example of generating the votes given Impartial Anonymous Culture
num_voters = 3
candidates = [1, 2, 3, 4, 5, 6]
list = generate_iac_voters(num_voters, candidates)
print(list)


vectors = [
    [5, 4, 3, 2, 1, 0],
    [1, 0.5, 0.33, 0.25, 0.2, 0.16]
]

c = calculate_borda_dominance(list, vectors)
print(c)