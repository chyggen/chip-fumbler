# Simulate a game with multiple agents, will make use of texasholdem game object
#
from typing import Tuple
from texasholdem.game.game import TexasHoldEm
from agent import Agent


# define some constants for setting up the game:
BUY_IN = 500
BIG_BLIND = 5
SMALL_BLIND = 0
MAX_PLAYERS = 2


def simulation_1v1(A0: Agent, A1: Agent, game_log: bool = False) -> Tuple[int, float]:
    """Runs a 1v1 simulation between two agents

    Args:
        A1: Agent 1
        A2: Agent 2
        game_log: if true, generate a game log

    Returns:
        A tuple containing: the winner, then a float indicating the
        winner's average chips gained / hand

    """
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
                game.take_action(*A0.action(game, random=True))
            else:
                game.take_action(*A1.action(game, random=True))
        if game_log:
            game.export_history("./pgns")  # save history

    # When we arrive here, the game is over.
    # We can determine who won by checking the active players in the pot:
    winner = list(game.in_pot_iter(game.btn_loc + 1))[0]
    chips_per_hand = BUY_IN / game.num_hands
    return(winner, chips_per_hand)


def round_robin(agents: list[Agent]) -> dict[Agent, float]:
    """Runs a round-robin tournament between a list of agents.

    Args:
        agents: a list of agents to enter into the tournament

    Returns:
        a dict containing a score for each agent.
    """
