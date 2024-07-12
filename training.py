import pygad
import numpy as np
import logging
import os
from datetime import datetime
import argparse

# Function to set up logging
def setup_logging():
    log_folder = "genetic_algorithm_logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_folder, f'ga_log_{timestamp}.txt')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Fitness function
def fitness_function(ga_instance, solution, solution_idx):
    fitness = np.sum(solution)  # Placeholder fitness function
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
    population = np.random.randint(2, size=(population_size, chromosome_length))

    logging.info(f'Initial population:\n{population}')

    # Compute and log the initial fitness values
    initial_fitness_values = [fitness_function(None, population[i], i) for i in range(population_size)]
    logging.info(f'Initial fitness values: {initial_fitness_values}\n')

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_function,
        sol_per_pop=population_size,
        num_genes=chromosome_length,
        initial_population=population,
        gene_type=int,  # Ensures genes remain integers
        mutation_percent_genes=10,  # Set mutation percentage
        on_generation=on_generation  # Callback function for logging each generation
    )

    ga_instance.run()
    ga_instance.plot_fitness()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    logging.info(f'Best solution: {solution}')
    logging.info(f'Best solution fitness: {solution_fitness}')

# Main execution block
if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Run a genetic algorithm.")
    parser.add_argument('--chromosome_length', type=int, default=10)
    parser.add_argument('--population_size', type=int, default=100)
    parser.add_argument('--num_generations', type=int, default=100)
    parser.add_argument('--num_parents_mating', type=int, default=20)

    args = parser.parse_args()

    CHROMOSOME_LENGTH = args.chromosome_length
    POPULATION_SIZE = args.population_size
    NUM_GENERATIONS = args.num_generations
    NUM_PARENTS_MATING = args.num_parents_mating

    run_genetic_algorithm(CHROMOSOME_LENGTH, POPULATION_SIZE, NUM_GENERATIONS, NUM_PARENTS_MATING)
