# Simulate a game with multiple agents, will make use of texasholdem game object
#
import itertools
from typing import Tuple
from texasholdem.game.game import TexasHoldEm

from agent import RandomAgent, Agent
from chromosome import Chromosome

from texasholdem import TexasHoldEm, HandPhase, ActionType

import concurrent.futures
from typing import List
from joblib import Parallel, delayed




# define some constants for setting up the game:
BUY_IN = 500
BIG_BLIND = 50
SMALL_BLIND = 25
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
    # A0 = RandomAgent(0)
    # A1 = RandomAgent(1)

    A0 = Agent(chromosome=C0)
    A1 = Agent(chromosome=C1)

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
                game.take_action(A0.action(game))
            elif game.current_player == 1:
                game.take_action(A1.action(game))
            else:
                print("Unexpected player turn.")
        if game_log:
            game.export_history("./pgns")  # save history

    winner = list(game.in_pot_iter(game.btn_loc + 1))[0]
    score = scoring(method=scoring_method, winner=winner, game=game)
    return (winner, score)


def round_robin(
    chromosomes: list[Chromosome], cycles: int = 1, scoring_method: str = "wins"
) -> list[float]:
    """Runs a round-robin tournament between a list of agents.

    Args:
        chromosomes: a list of chromosomes to enter into the tournament
        cycles: how many matches each agent plays against every other agent
        scoring_method: a string specifying how game scores are determined.

    Returns:
        a dict containing a score for each agent.
    """
    scores = [0 for _ in range(len(chromosomes))]
    
    chromosome_indecies = [i for i in range(len(chromosomes))]
    chromosome_index_pairs = list(itertools.combinations(chromosome_indecies, 2))

    for _ in range(cycles):
        for I0, I1 in chromosome_index_pairs:
            C0 = chromosomes[I0]
            C1 = chromosomes[I1]
            (winner, score) = simulation_1v1(C0, C1, scoring_method=scoring_method)
            if winner == 0:
                scores[I0] += score
                scores[I1] -= score
            else:
                scores[I1] += score
                scores[I0] -= score

    return scores

def play_matches(
    chromosomes: List[Chromosome], target_idx: int, cycles: int = 1, scoring_method: str = "wins", n_jobs: int = -1
) -> float:
    C0 = chromosomes[target_idx]
    
    def play_single_match(C0: Chromosome, opponent: Chromosome) -> float:
        (winner, score) = simulation_1v1(C0, opponent, scoring_method=scoring_method)
        return score if winner == 0 else 0
    
    all_scores = Parallel(n_jobs=n_jobs)(
        delayed(play_single_match)(C0, opponent)
        for _ in range(cycles)
        for index, opponent in enumerate(chromosomes) if index != target_idx
    )
    
    final_score = sum(all_scores)
    return final_score
            
    