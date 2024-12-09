from IAC import generate_iac_voters
from IC import generate_ic_voters
from spatial import spatial
from Borda import generateBordaVector, findBordaWinner
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
    
    findBordaWinner(borda_vector, num_candidates, population)
    
    precedence_table = buildPrecedenceTable(num_candidates, population)
    
    condorcet_winner, condorcet_loser = getCondorcetWinnerLoser(precedence_table, num_candidates)
    
    full_result = fullCondorcet(num_candidates, population)

    borda_dominance = calculate_borda_dominance(population, [borda_vector])
    
    return {
        'population': population,
        'borda_vector': borda_vector,
        'condorcet_winner': condorcet_winner,
        'condorcet_loser': condorcet_loser,
        'full_condorcet_result': full_result,
        'borda_dominance': borda_dominance
    }

def main():
    candidate_counts = [3, 4, 5, 6]
    voting_models = ['IAC', 'IC', 'Spatial']
    scoring_types = ['linear', 'inverse']
    powers = [1, 2, 3]
    num_voters = 1000 
    num_simulations = 10  # Number of times to repeat each experiment

    # Nested loop to run all combinations
    for num_candidates in candidate_counts:
        print(f"\n--- {num_candidates} Candidates Simulation ---")
        for voting_model in voting_models:
            for scoring_type in scoring_types:
                for power in powers:
                    print(f"\nModel: {voting_model}, Scoring: {scoring_type}, Power: {power}")
                    
                    # Run multiple simulations
                    simulation_results = [
                        run_simulation(num_candidates, num_voters, voting_model, scoring_type, power)
                        for _ in range(num_simulations)
                    ]
                    
                    condorcet_winners = [result['condorcet_winner'] for result in simulation_results]
                    condorcet_losers = [result['condorcet_loser'] for result in simulation_results]
                    borda_dominance_results = [result['borda_dominance'] for result in simulation_results]
                    
                    print(f"Condorcet Winners: {condorcet_winners}")
                    print(f"Condorcet Losers: {condorcet_losers}")
                    print(f"Borda Dominance Results: {borda_dominance_results}") # figure out how to best show this data
                    # We can do other printing / analaysis of data here

if __name__ == "__main__":
    main()