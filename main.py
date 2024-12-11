from IAC import generate_iac_voters
from IC import generate_ic_voters
from spatial import spatial
from Borda import generateBordaVector, findBordaWinner, CERVONE_CONSTANT
from condorcet import fullCondorcet, buildPrecedenceTable, getCondorcetWinnerLoser
from borda_dominance import calculate_borda_dominance

def run_simulation(num_candidates, num_voters, voting_model, scoring_type, power):
    if voting_model == 'IAC':
        population = generate_iac_voters(num_voters, num_candidates)
    elif voting_model == 'IC':
        population = generate_ic_voters(num_voters, num_candidates)
    elif voting_model == 'Spatial':
        population = spatial(num_voters, num_candidates)
    else:
        raise ValueError(f"Unknown voting model: {voting_model}")
    
    borda_vector = generateBordaVector(scoring_type, num_candidates, power)
    
    borda_winner = findBordaWinner(borda_vector, num_candidates, population)
    
    condorcet_winner, condorcet_loser, full_result = fullCondorcet(num_candidates, population)
    print(full_result)

    borda_dominance = calculate_borda_dominance(population, [borda_vector])
    
    return {
        'population': population,
        'borda_vector': borda_vector,
        'borda_winner': borda_winner,
        'condorcet_winner': condorcet_winner,
        'condorcet_loser': condorcet_loser,
        'full_condorcet_result': full_result,
        'borda_dominance': borda_dominance
    }

def main():
    candidate_counts = [3, 4, 5, 6]
    voting_models = ['IAC', 'IC', 'Spatial']
    scoring_types = ['linear', 'inverse']
    powers = [1/3, 1/2, 1, CERVONE_CONSTANT, 2, 3]
    num_voters = 1000 
    num_simulations = 100  # Number of times to repeat each experiment

    #[Candidate Count - 3][Voting Model][Condorcet winner existance/Dominates/IsDominated][Domated/Dominating count]
    #For the third parameter, 0 is existance, 1 is domates, and 2 is being dominated
    borda_vs_condorcetWin = [[[[0 for _ in range(candidate_counts[-1])] for _ in range(3)] for _ in voting_models] for _ in candidate_counts]
    borda_vs_condorcetLose = [[[[0 for _ in range(candidate_counts[-1])] for _ in range(3)] for _ in voting_models] for _ in candidate_counts]
    #[Candidate Count -3][Voting Model][Power][Linear/Inverse]
    vector_vs_condorcet = [[[[0 for _ in scoring_types] for _ in powers] for _ in voting_models] for _ in candidate_counts]
    vector_vs_condorcetExist = [[[[0 for _ in scoring_types] for _ in powers] for _ in voting_models] for _ in candidate_counts]
    vector_vs_copeland = [[[[0 for _ in scoring_types] for _ in powers] for _ in voting_models] for _ in candidate_counts]

    # Nested loop to run all combinations
    for num_candidates in candidate_counts:
        print(f"\n--- {num_candidates} Candidates Simulation ---")
        for voting_model in voting_models:
            for scoring_type in scoring_types:
                for power in powers:
                    if scoring_type=="inverse" and power==CERVONE_CONSTANT:
                        continue
                    print(f"\nModel: {voting_model}, Scoring: {scoring_type}, Power: {power}")
                    
                    # Run multiple simulations
                    simulation_results = [
                        run_simulation(num_candidates, num_voters, voting_model, scoring_type, power)
                        for _ in range(num_simulations)
                    ]
                    
                    condorcet_winners = [result['condorcet_winner'] for result in simulation_results]
                    condorcet_losers = [result['condorcet_loser'] for result in simulation_results]
                    borda_winners = [result['borda_winner'] for result in simulation_results]
                    borda_dominance_results = [result['borda_dominance'] for result in simulation_results]


                    for i in range(num_simulations):
                        vector_vs_copeland[num_candidates-3][voting_models.index(voting_model)][powers.index(power)][scoring_types.index(scoring_type)] += simulation_results[i]['full_condorcet_result'][borda_winners[i]]

                        #Counts the number of condorcet winners
                        if condorcet_winners[i] != -1:
                            vector_vs_condorcetExist[num_candidates-3][voting_models.index(voting_model)][powers.index(power)][scoring_types.index(scoring_type)] += 1
                            if borda_winners[i] == condorcet_winners[i]:
                                vector_vs_condorcet[num_candidates-3][voting_models.index(voting_model)][powers.index(power)][scoring_types.index(scoring_type)] += 1

                            borda_vs_condorcetWin[num_candidates -3][voting_models.index(voting_model)][0][0] += 1
                            print(num_candidates, voting_model)
                            print(borda_vs_condorcetWin[num_candidates -3][voting_models.index(voting_model)][0][0])
                            borda_vs_condorcetWin[num_candidates -3][voting_models.index(voting_model)][1][len(borda_dominance_results[i][condorcet_winners[i]])] += 1
                            dominated_count = 0
                            for vector in borda_dominance_results[i]:
                                if (condorcet_winners[i]-1) in vector:
                                    dominated_count += 1
                            borda_vs_condorcetWin[num_candidates -3][voting_models.index(voting_model)][2][dominated_count] += 1

                        if condorcet_losers[i] != -1:
                            borda_vs_condorcetLose[num_candidates -3][voting_models.index(voting_model)][0][0] += 1
                            borda_vs_condorcetLose[num_candidates -3][voting_models.index(voting_model)][1][len(borda_dominance_results[i][condorcet_losers[i]])] += 1
                            dominated_count = 0
                            for vector in borda_dominance_results[i]:
                                if (condorcet_losers[i]-1) in vector:
                                    dominated_count += 1
                            borda_vs_condorcetLose[num_candidates -3][voting_models.index(voting_model)][2][dominated_count] += 1
                
                    print(f"Condorcet Winners: {condorcet_winners}")
                    print(f"Condorcet Losers: {condorcet_losers}")
                    print(f"Borda Dominance Results: {borda_dominance_results}") # figure out how to best show this data
                    # We can do other printing / analaysis of data here
    print()
    print("CONDORCET WINNER vs BORDA DOMINANCE")
    print("\t\tH\tJ-0\tJ-1\tJ-2\tJ-3\tJ-4\tJ-5\tK-0\tK-1\tK-2\tK-3\tK-4\tK-5")
    for i in range(len(candidate_counts)):
        for j in range(len(voting_models)):
            if j==2:
                print("SPAT-"+str(candidate_counts[i]) +"\t\t", end="")
            else:
                print(voting_models[j]+"-"+str(candidate_counts[i]) +"\t\t", end="")
            print("%.2f" % (borda_vs_condorcetWin[i][j][0][0]/(num_simulations* len(scoring_types) * len(powers))), end="\t")
            for k in range(candidate_counts[-1]):
                if k >=i+3:
                    print("--", end="\t")
                else:
                    print("%.2f" % (borda_vs_condorcetWin[i][j][1][k]/borda_vs_condorcetWin[i][j][0][0]), end="\t")
            for k in range(candidate_counts[-1]):
                if k >=i+3:
                    print("--", end="\t")
                else:
                    print("%.2f" % (borda_vs_condorcetWin[i][j][2][k]/borda_vs_condorcetWin[i][j][0][0]), end="\t")
            print()

    print()
    print("CONDORCET LOSER vs BORDA DOMINANCE")
    print("\t\tP\tQ-0\tQ-1\tQ-2\tQ-3\tQ-4\tQ-5\tR-0\tR-1\tR-2\tR-3\tR-4\tR-5")
    for i in range(len(candidate_counts)):
        for j in range(len(voting_models)):
            if j==2:
                print("SPAT-"+str(candidate_counts[i]) +"\t\t", end="")
            else:
                print(voting_models[j]+"-"+str(candidate_counts[i]) +"\t\t", end="")
            print("%.2f" % (borda_vs_condorcetLose[i][j][0][0]/(num_simulations* len(scoring_types) * len(powers))), end="\t")
            for k in range(candidate_counts[-1]):
                if k >=i+3:
                    print("--", end="\t")
                else:
                    print("%.2f" % (borda_vs_condorcetLose[i][j][2][k]/borda_vs_condorcetLose[i][j][0][0]), end="\t")
            for k in range(candidate_counts[-1]):
                if k >=i+3:
                    print("--", end="\t")
                else:
                    print("%.2f" % (borda_vs_condorcetLose[i][j][1][k]/borda_vs_condorcetLose[i][j][0][0]), end="\t")
            print()

    print("Scoring Vectors vs Condorcet")
    print("\t\tL/3\tI/3\tL/2\tI/2\tL\tI\tCv\tL2\tI2\tL3\tI3")
    for i in range(len(candidate_counts)):
        for j in range(len(voting_models)):
            if j==2:
                print("SPAT-"+str(candidate_counts[i]) +"\t\t", end="")
            else:
                print(voting_models[j]+"-"+str(candidate_counts[i]) +"\t\t", end="")
            for k in range(len(powers)):
                for l in range(len(scoring_types)):
                    if k==3 and l ==1:
                        continue
                    print("%.2f" % (vector_vs_condorcet[i][j][k][l]/vector_vs_condorcetExist[i][j][k][l]), end="\t")
            print()

    print("Scoring Vectors vs Expected Copeland Deficiency")
    print("\t\tL/3\tI/3\tL/2\tI/2\tL\tI\tCv\tL2\tI2\tL3\tI3")
    for i in range(len(candidate_counts)):
        for j in range(len(voting_models)):
            if j==2:
                print("SPAT-"+str(candidate_counts[i]) +"\t\t", end="")
            else:
                print(voting_models[j]+"-"+str(candidate_counts[i]) +"\t\t", end="")
            for k in range(len(powers)):
                for l in range(len(scoring_types)):
                    if k==3 and l ==1:
                        continue
                    print("%.2f" % (vector_vs_copeland[i][j][k][l]/num_simulations), end="\t")
            print()

if __name__ == "__main__":
    main()