import pygad
import numpy as np
import logging
import os
from datetime import datetime
import argparse
from chromosome import Chromosome
from simulation import simulation_1v1, round_robin
from agent import Agent  # Import the Agent class
from pathlib import Path

# Function to set up logging
def setup_logging():
    log_folder = "genetic_algorithm_logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_folder, f'ga_log_{timestamp}.txt')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Fitness function
def fitness_function(ga_instance, solution, solution_idx, wins_dict):
    chromosome = Chromosome(
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

    # The fitness is the number of wins for this chromosome
    fitness = wins_dict.get(chromosome, 0)
    print(fitness)
    logging.info(f'Solution: {chromosome}, Fitness: {fitness}')
    return fitness

# Callback function called after each generation
def on_generation(ga_instance):
    population = ga_instance.population
    fitness_values = ga_instance.last_generation_fitness

    logging.info(f'Generation {ga_instance.generations_completed}')
    logging.info(f'Population:\n{population}')
    logging.info(f'Fitness values: {fitness_values}\n')

# Runs the genetic algorithm
def run_genetic_algorithm(chromosome_length, population_size, num_generations, num_parents_mating):
    # Initialize the population using the Chromosome class
    initial_population = [Chromosome.random() for _ in range(population_size)]
    population = np.array([[chromosome.aggressiveness_preflop, chromosome.aggressiveness_flop, chromosome.aggressiveness_turn,
                            chromosome.aggressiveness_river, chromosome.bluff_probability_preflop, chromosome.bluff_probability_flop,
                            chromosome.bluff_probability_turn, chromosome.bluff_probability_river, chromosome.tightness_vs_looseness,
                            chromosome.dynamic_vs_static, chromosome.bet_size_variability] for chromosome in initial_population])

    logging.info(f'Initial population:\n{population}')

    # Compute initial wins using round robin
    agents = [Agent(chromosome) for chromosome in initial_population]
    wins_dict = round_robin(agents)

    # Compute and log the initial fitness values
    initial_fitness_values = [fitness_function(None, population[i], i, wins_dict) for i in range(population_size)]
    logging.info(f'Initial fitness values: {initial_fitness_values}\n')

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=lambda ga, sol, idx: fitness_function(ga, sol, idx, wins_dict),
        sol_per_pop=population_size,
        num_genes=chromosome_length,
        initial_population=population,
        gene_type=float,  # Ensures genes remain floats
        mutation_percent_genes=10,  # Set mutation percentage
        on_generation=on_generation  # Callback function for logging each generation
    )

    ga_instance.run()
    ga_instance.plot_fitness()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    logging.info(f'Best solution: {solution}')
    logging.info(f'Best solution fitness: {solution_fitness}')

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
    parser.add_argument('-p', '--population_size', type=int, default=10, help="Size of the population")
    parser.add_argument('-n', '--num_generations', type=int, default=100, help="Number of generations")
    parser.add_argument('-m', '--num_parents_mating', type=int, default=4, help="Number of parents mating")

    args = parser.parse_args()

    CHROMOSOME_LENGTH = args.chromosome_length
    POPULATION_SIZE = args.population_size
    NUM_GENERATIONS = args.num_generations
    NUM_PARENTS_MATING = args.num_parents_mating

    run_genetic_algorithm(CHROMOSOME_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, NUM_PARENTS_MATING)
