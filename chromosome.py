from pathlib import Path
from dataclasses import dataclass


@dataclass
class Chromosome:
    aggressiveness: float
    bluff_probability: float

    # Parse Chromosome from file
    def from_file(file: Path):
        pass

    # Store the chromosome in a file
    def to_file(self, destination: Path):
        pass

    # Generate a random chromosome
    def random():
        pass
