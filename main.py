# Teancum, Jared, & Ryan
# 5110 Final project

import random
from IAC import generate_iac_voters
from IC import generate_ic_voters
from spatial import spatial
from Borda import generateBordaVector, findBordaWinner
from condorcet import fullCondorcet, buildPrecedenceTable, getCondorcetWinnerLoser

def run_simulation(num_candidates, num_voters, voting_model, scoring_type, power):
    # Generate population based on voting model
    candidates = list(range(num_candidates))
    
    if voting_model == 'IAC':
        population = generate_iac_voters(num_voters, num_candidates)
    elif voting_model == 'IC':
        population = generate_ic_voters(num_voters, num_candidates)
    elif voting_model == 'Spatial':
        # Spatial model returns rankings, needs to be converted to population format
        rankings = spatial(num_voters, candidates)
        # Convert rankings to population format with equal group sizes
        population = [(tuple(rank), 1) for rank in rankings]
    else:
        raise ValueError(f"Unknown voting model: {voting_model}")

    # Generate Borda vector
    borda_vector = generateBordaVector(scoring_type, num_candidates, power)
    
    # Find Borda winner
    findBordaWinner(borda_vector, num_candidates, population)
    
    # Build precedence table for Condorcet analysis
    precedence_table = buildPrecedenceTable(num_candidates, population)
    
    # Get Condorcet winner and loser
    condorcet_winner, condorcet_loser = getCondorcetWinnerLoser(precedence_table, num_candidates)
    
    # Full Condorcet analysis
    full_result = fullCondorcet(num_candidates, population)
    
    return {
        'population': population,
        'borda_vector': borda_vector,
        'condorcet_winner': condorcet_winner,
        'condorcet_loser': condorcet_loser,
        'full_condorcet_result': full_result
    }

def main():
    # Experimental parameters
    candidate_counts = [3, 4, 5, 6]
    voting_models = ['IAC', 'IC', 'Spatial']
    scoring_types = ['linear', 'inverse']
    powers = [1, 2, 3]  # Different power values to explore
    num_voters = 1000  # Number of voters per simulation
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
                    
                    # Basic result aggregation (you can expand this)
                    borda_winners = [result['condorcet_winner'] for result in simulation_results]
                    print(f"Condorcet Winners: {borda_winners}")

if __name__ == "__main__":
    main()