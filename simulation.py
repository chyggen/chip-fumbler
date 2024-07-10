# Simulate a game with multiple agents, will make use of texasholdem game object
#
from typing import Tuple
from texasholdem.game.game import TexasHoldEm
from agent import Agent


def simulation_1v1(A1: Agent, A2: Agent) -> Tuple[bool, float]:
    """Runs a 1v1 simulation between two agents

    Args:
        A1: Agent 1
        A2: Agent 2

    Returns:
        A tuple containing: A bool indicating if A1 won, then a float indicating the
        winner's average chips gained / hand

    """
    pass


def round_robin(agents: list[Agent]) -> dict[Agent, float]:
    """Runs a round-robin tournament between a list of agents.

    Args:
        agents: a list of agents to enter into the tournament

    Returns:
        a dict containing a score for each agent.
    """
    pass
