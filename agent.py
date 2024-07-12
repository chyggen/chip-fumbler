from typing import Tuple, Optional

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent

from chromosome import Chromosome


class Agent:

    # Create an agent based on a chromosome
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome

    # Decide the next move based on the game state and the agent's chromosome
    # Returns the action to take, plus a number of chips if the action is a raise
    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        pass

    # Get the agent's underlying chromosome
    def get_chromosome(self) -> Chromosome:
        return self.chromosome


# A child class that makes random moves, used for testing
class RandomAgent(Agent):
    def __init__(self, id):
        # since random agents do not have a chromosome, they need an ID to be 
        # differentiable from other random agents
        self.id = id
        pass

    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        return random_agent(game)

    def get_chromosome(self) -> None:
        return None
