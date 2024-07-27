from chromosome import Chromosome
from simulation import simulation_1v1, round_robin

def main():
    # Generate two random chromosomes
    chromosome1 = Chromosome.random()
    chromosome2 = Chromosome.random()

    print("Chromosome 1:", chromosome1)
    print("Chromosome 2:", chromosome2)

    # Run a 1v1 simulation
    winner, score = simulation_1v1(chromosome1, chromosome2, game_log=True, scoring_method="wins")

    # Output the results
    print(f"Winner: {'Agent 1' if winner == 0 else 'Agent 2'} - Score: {score}")

if __name__ == "__main__":
    main()
