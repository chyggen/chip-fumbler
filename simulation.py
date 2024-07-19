# Simulate a game with multiple agents, will make use of texasholdem game object
#
import itertools
from typing import Tuple
from texasholdem.game.game import TexasHoldEm

from agent import Agent, RandomAgent
from chromosome import Chromosome


# define some constants for setting up the game:
BUY_IN = 500
BIG_BLIND = 5
SMALL_BLIND = 0
MAX_PLAYERS = 2


def scoring(method: str, winner: int, game: TexasHoldEm) -> float:
    """Defines how the agents are scored

    Args:
        method: The method used for scoring
        winner: The index of the agent who won
        game: The texasholdem game object

    Returns:
        a score
    """
    if method == "wins":
        return 1
    elif method == "chips per hand":
        return BUY_IN / game.num_hands
    else:
        raise ValueError("Invalid scoring method")


def simulation_1v1(
    C0: Chromosome, C1: Chromosome, game_log: bool = False, scoring_method: str = "wins"
) -> Tuple[int, float]:
    """Runs a 1v1 simulation between two agents
    Args:
        C0: chromosome used to make agent 0
        C1: chromosome used to make agent 1
        game_log: if true, generate a game log
        scoring_method: string to describe how games are scored. refer to scoring function

    Returns:
        A tuple containing: the winner, then a float indicating the
        winner's average chips gained / hand

    """

    # TODO: make this actually use real agents and chromosomes when our descision algorithm works
    A0 = RandomAgent(0)
    A1 = RandomAgent(1)

    game = TexasHoldEm(
        buyin=BUY_IN,
        big_blind=BIG_BLIND,
        small_blind=SMALL_BLIND,
        max_players=MAX_PLAYERS,
    )
    while game.is_game_running():
        game.start_hand()
        while game.is_hand_running():
            if game.current_player == 0:
                game.take_action(*A0.action(game))
            else:
                game.take_action(*A1.action(game))
        if game_log:
            game.export_history("./pgns")  # save history

    # When we arrive here, the game is over.
    # We can determine who won by checking the active players in the pot:
    winner = list(game.in_pot_iter(game.btn_loc + 1))[0]
    score = scoring(method=scoring_method, winner=winner, game=game)
    return (winner, score)


def round_robin(
    chromosomes: list[Chromosome], cycles: int = 1, scoring_method: str = "wins"
) -> dict[Agent, float]:
    """Runs a round-robin tournament between a list of agents.

    Args:
        chromosomes: a list of chromosomes to enter into the tournament
        cycles: how many matches each agent plays against every other agent
        scoring_method: a string specifying how game scores are determined.

    Returns:
        a dict containing a score for each agent.
    """

    # initialize a dict to store agent scores in
    scores = {chromosome: 0 for chromosome in chromosomes}

    # generate all possible agent pairs
    chromosome_pairs = list(itertools.combinations(chromosomes, 2))

    for _ in range(cycles):
        for C0, C1 in chromosome_pairs:
            (winner, score) = simulation_1v1(C0, C1, scoring_method=scoring_method)
            if winner == 0:
                scores[C0] += score
                scores[C1] -= score
            else:
                scores[C0] -= score
                scores[C1] += score

    return scores
