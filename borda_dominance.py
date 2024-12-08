# input: a list of tuples including rank and number of votes for given rank and a list of scoring vectors

# output: a lists of list where position index + 1 is the candidate
# and items in index are dominated by that candidate

def calculate_borda_dominance(voter_data, scoring_vectors):
    dominated = sorted(voter_data[0][0])
    score_results = []
    for i in range(len(scoring_vectors)):
        result = get_vector_result(voter_data, scoring_vectors[i])
        score_results.append(result)

    r = check_borda_dominance(score_results)
    return r

def get_vector_result(voter_data, scoring_vector):
    num_candidates = len(voter_data[0][0])
    result = [0] * num_candidates

    # update each candidate's awarded points
    for vr in voter_data:
        ranking = vr[0]
        votes = vr[1]
        for i in range(num_candidates):
            index = ranking[i] - 1
            points_awarded = scoring_vector[i]
            result[index] += votes * points_awarded

    result = [round(num, 2) for num in result]
    return result


def dominates(candidate1, candidate2, scores_list):
    for scores in scores_list:
        if scores[candidate1 - 1] < scores[candidate2 - 1]:
            return False  # If candidate1 scores less in any score vector, it doesn't dominate
    # Check for at least one strict inequality
    return any(scores[candidate1 - 1] > scores[candidate2 - 1] for scores in scores_list)


def check_borda_dominance(scores_list):
    num_candidates = len(scores_list[0])  # Number of candidates
    dominance_results = [[] for _ in range(num_candidates)]  # Initialize dominance results

    # Check dominance for all pairs of candidates
    for i in range(1, num_candidates + 1):  # Candidate 1 to num_candidates
        for j in range(1, num_candidates + 1):  # Compare against all candidates
            dominate = dominates(i, j, scores_list)
            if i != j and dominate:
                dominance_results[i - 1].append(j)

    return dominance_results