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
    def action(
        self, game: TexasHoldEm, random: bool = False
    ) -> Tuple[ActionType, Optional[int]]:
        if random:
            return random_agent(game)
        else:
            pass

    # Get the agent's underlying chromosome
    def get_chromosome(self) -> Chromosome:
        return self.chromosome
