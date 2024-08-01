import pygad
import numpy as np
import logging
import os
from datetime import datetime
import argparse
from chromosome import Chromosome
from simulation import simulation_1v1, round_robin, play_matches
from agent import Agent
from pathlib import Path
import tqdm
import random



# Function to set up logging
def setup_logging():
    log_folder = "genetic_algorithm_logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_folder, f'ga_log_{timestamp}.txt')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='\n %(message)s')

# Fitness function
def fitness_function(ga_instance, solution, solution_idx):

    chromosomes = [Chromosome(
        aggressiveness_preflop=c[0],
        aggressiveness_flop=c[1],
        aggressiveness_turn=c[2],
        aggressiveness_river=c[3],
        bluff_probability_preflop=c[4],
        bluff_probability_flop=c[5],
        bluff_probability_turn=c[6],
        bluff_probability_river=c[7],
        tightness_vs_looseness=c[8],
        dynamic_vs_static=c[9],
        bet_size_variability=c[10]
    ) for c in ga_instance.population]

    #score = ga_instance.score_cache[solution_idx]
    score = play_matches(chromosomes, solution_idx)
    #logging.info(f'SOLUTION INDEX: {solution_idx}, SCORE: {score}')

    logging.info(f'SOLUTION: {solution}, SCORE: {score}')
    #print(score)

    #logging.info(f'SCORE CACHE: {ga_instance.score_cache}')

    #logging.info(f'SOLUTION: {solution}, INDEX: {solution_idx}')

    return score

# Callback function called after each generation
def on_generation(ga_instance, pbar):

    # chromosomes = [Chromosome(
    #     aggressiveness_preflop=c[0],
    #     aggressiveness_flop=c[1],
    #     aggressiveness_turn=c[2],
    #     aggressiveness_river=c[3],
    #     bluff_probability_preflop=c[4],
    #     bluff_probability_flop=c[5],
    #     bluff_probability_turn=c[6],
    #     bluff_probability_river=c[7],
    #     tightness_vs_looseness=c[8],
    #     dynamic_vs_static=c[9],
    #     bet_size_variability=c[10]
    # ) for c in ga_instance.population]

    #scores = round_robin(chromosomes)
    #ga_instance.score_cache = scores

    current_population = ga_instance.population
    fitness_values = ga_instance.last_generation_fitness
    logging.info('------------------------------------------------')
    logging.info(f'Generation {ga_instance.generations_completed}')
    logging.info(f'{current_population}')
    #logging.info(f'Scores: {ga_instance.score_cache}\n')


    #logging.info(chromosomes)

    #test = ga_instance.
    #logging.info(test)

    #logging.info(f'Generation {ga_instance.generations_completed}')
    #logging.info(f'{current_population}\n')
    #logging.info(f'SOLUTION: {ga_instance.solution[0]}')

    # logging.info(f'Fitness values: {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}')

    #chromosomes = [Chromosome(*gene) for gene in population]

    #current_chromosome = [
    # Chromosome(
    #     aggressiveness_preflop=sol[0],
    #     aggressiveness_flop=sol[1],
    #     aggressiveness_turn=sol[2],
    #     aggressiveness_river=sol[3],
    #     bluff_probability_preflop=sol[4],
    #     bluff_probability_flop=sol[5],
    #     bluff_probability_turn=sol[6],
    #     bluff_probability_river=sol[7],
    #     tightness_vs_looseness=sol[8],
    #     dynamic_vs_static=sol[9],
    #     bet_size_variability=sol[10]
    # ) for sol in current_population]

    # # Re-evaluate wins and losses
    # chromosomes = [Chromosome(*gene) for gene in population]
    #wins_dict, losses_dict = round_robin(chromosomes)
    # total_fitness = sum(new_wins_dict.values()) - sum(new_losses_dict.values())
    #wins_dict, losses_dict = round_robin(current_chromosome)

    #logging.info(f'Generation {ga_instance.generations_completed}: Wins: {wins_dict}, Losses: {losses_dict}')

    # fitness_values = []
    # for i in range(population_size):
    #     fitness = fitness_function(None, population[i], i, wins_dict, losses_dict)
    #     fitness_values.append(fitness)  

    #logging.info(f'New fitness values: {fitness_values}\n')

    # solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # logging.info(f'Best solution: {solution}')
    # logging.info(f'Best solution fitness: {solution_fitness}')

    # # # Update wins_dict and losses_dict
    # wins_dict.clear()
    # losses_dict.clear()
    # wins_dict.update(new_wins_dict)
    # losses_dict.update(new_losses_dict)

    pbar.update(1)  # Update the progress bar for each generation

# Runs the genetic algorithm
def run_genetic_algorithm(chromosome_length, population_size, num_generations, num_parents_mating):
    # Initialize the population using the Chromosome class
    initial_population = [Chromosome.random() for _ in range(population_size)]
    initial_array_population = np.array([[chromosome.aggressiveness_preflop, 
                            chromosome.aggressiveness_flop, 
                            chromosome.aggressiveness_turn,
                            chromosome.aggressiveness_river, 
                            chromosome.bluff_probability_preflop, 
                            chromosome.bluff_probability_flop,
                            chromosome.bluff_probability_turn, 
                            chromosome.bluff_probability_river, 
                            chromosome.tightness_vs_looseness,
                            chromosome.dynamic_vs_static, 
                            chromosome.bet_size_variability] for chromosome in initial_population])

    #logging.info(f'Initial Population: {population}')

    # # # Compute initial wins and losses using round robin
    # wins_dict, losses_dict = round_robin(initial_population)

    # # # Compute initial fitness values using the wins and losses dictionary
    # initial_fitness_values = []
    # for i in range(population_size):
    #     fitness = fitness_function(None, population[i], i, wins_dict, losses_dict)
    #     initial_fitness_values.append(fitness)

    # total_fitness = sum(initial_fitness_values)
    # if total_fitness != 0:
    #     logging.error(f'Total initial fitness is not zero: {total_fitness}')
    #     raise ValueError(f'Total initial fitness is not zero: {total_fitness}')

    #logging.info(f'Initial fitness values: {initial_fitness_values}\n')

    pbar = tqdm.tqdm(total=num_generations)  # Initialize the progress bar

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=lambda ga, sol, idx: fitness_function(ga, sol, idx),
        sol_per_pop=population_size,
        num_genes=chromosome_length,
        initial_population=initial_array_population,
        gene_type=float,  # Ensures genes remain floats
        mutation_percent_genes=10,  # Set mutation percentage to 20% for higher diversity
        # mutation_type="random",  # Mutation type to random
        on_generation=lambda ga: on_generation(ga, pbar),  # Callback function for logging each generation
        # crossover_probability=0.9,  # Set crossover probability
        # parent_selection_type="rank",  # Use rank selection
        keep_parents=2,  # Keep top 2 parents for the next generation
        # crossover_type="single_point",  # Use single point crossover
        gene_space={'low': 0.0, 'high': 1.0, 'step': 0.001}  # Ensure genes remain in [0, 1] range
    )

    ga_instance.score_cache = [0] * population_size

    ga_instance.run()
    #ga_instance.plot_fitness()
    pbar.close()  # Close the progress bar when the genetic algorithm is done


     # Retrieve and log the best solution
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    logging.info(f'Best solution: {solution}')
    logging.info(f'Best solution fitness: {solution_fitness}')
    logging.info(f'Best solution index: {solution_idx}')



    # Save the best solution as a Chromosome
    best_chromosome = Chromosome(
        aggressiveness_preflop=solution[0],
        aggressiveness_flop=solution[1],
        aggressiveness_turn=solution[2],
        aggressiveness_river=solution[3],
        bluff_probability_preflop=solution[4],
        bluff_probability_flop=solution[5],
        bluff_probability_turn=solution[6],
        bluff_probability_river=solution[7],
        tightness_vs_looseness=solution[8],
        dynamic_vs_static=solution[9],
        bet_size_variability=solution[10]
    )
    best_chromosome.to_file(Path('best_chromosomes'))

# Main execution block
if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Run a genetic algorithm.")
    parser.add_argument('-l', '--chromosome_length', type=int, default=11, help="Length of the chromosome")
    parser.add_argument('-p', '--population_size', type=int, default=20, help="Size of the population")
    parser.add_argument('-n', '--num_generations', type=int, default=100, help="Number of generations")
    parser.add_argument('-m', '--num_parents_mating', type=int, default=2, help="Number of parents mating")

    args = parser.parse_args()

    CHROMOSOME_LENGTH = args.chromosome_length
    POPULATION_SIZE = args.population_size
    NUM_GENERATIONS = args.num_generations
    NUM_PARENTS_MATING = args.num_parents_mating

    run_genetic_algorithm(CHROMOSOME_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, NUM_PARENTS_MATING)
