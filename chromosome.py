from dataclasses import dataclass, asdict
import random
import json
from datetime import datetime
from pathlib import Path

@dataclass
class Chromosome:

    # An aggressive agent will be more likely to make large bets
    # ex) 
    # a 1.000 aggressiveness agent will always raise
    # a 0.000 aggressiveness agent will usually call/fold  
    aggressiveness_preflop: float
    aggressiveness_flop: float
    aggressiveness_turn: float
    aggressiveness_river: float

    # A high bluff probability agent will be more likely to play a bad hand to bluff an opponent
    # ex)
    # a 1.000 bluff probability agent will always bluff
    # a 0.000 bluff probability agent will never bluff
    bluff_probability_preflop: float
    bluff_probability_flop: float
    bluff_probability_turn: float
    bluff_probability_river: float

    # A high tightness agent will play a smaller number of only the best hands.
    # ex)
    # a 1.000 tightness agent will only ever play the nuts 
    # a 0.000 tightness agent will play every hand
    tightness_vs_looseness: float

    # A dynamic agent will be more likely to alter their strategy (more randomness in bets)
    # ex)
    # a 1.000 dynamic agent will have a basically random strategy
    # a 0.000 dynamic agent will never adjust their strategy (no randomness)
    dynamic_vs_static: float

    # An agent with high bet size variability will have a bet size that varies a lot hand to hand
    # ex)
    # a 1.000 bet size variability agent will swing their bets over a large range
    # a 0.000 bet size variability agent will only bet the same amounts each time they play
    bet_size_variability: float

    @staticmethod
    def random():
        """
        Generate a random Chromosome with each behavior being ranked 1.000 to 0.000
        """
        return Chromosome(
            aggressiveness_preflop=round(random.uniform(0, 1), 3),
            aggressiveness_flop=round(random.uniform(0, 1), 3),
            aggressiveness_turn=round(random.uniform(0, 1), 3),
            aggressiveness_river=round(random.uniform(0, 1), 3),
            bluff_probability_preflop=round(random.uniform(0, 1), 3),
            bluff_probability_flop=round(random.uniform(0, 1), 3),
            bluff_probability_turn=round(random.uniform(0, 1), 3),
            bluff_probability_river=round(random.uniform(0, 1), 3),
            tightness_vs_looseness=round(random.uniform(0, 1), 3),
            dynamic_vs_static=round(random.uniform(0, 1), 3),
            bet_size_variability=round(random.uniform(0, 1), 3)
        )

    def to_file(self, directory: Path):
        """
        Save the Chromosome to a JSON file with the current date and time as the filename.
        """
        directory.mkdir(parents=True, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
        filepath = directory / filename
        with filepath.open('w') as f:
            json.dump(asdict(self), f, indent=4)

# Example usage
# Generate a random chromosome
chromosome = Chromosome.random()

# Save the chromosome to a file in the "chromosomes" folder
directory = Path('chromosomes')
chromosome.to_file(directory)
