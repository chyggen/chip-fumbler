# This file creates a player vs agents game using the texasholdem GUI

# currently, the table has 6 players:
# - 1 user
# - 5 random agents

import argparse
from pathlib import Path

from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agent import Agent
from chromosome import Chromosome
from pprint import pprint
from time import sleep

DEBUG = False

def run_game(chromosome: Chromosome):

    game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=2)
    gui = TextGUI(game=game, visible_players=[0])

    opponent = Agent(chromosome)

    while game.is_game_running():
        game.start_hand()

        while game.is_hand_running():
            if game.current_player == 0:
                gui.run_step()

            else:
                gui.display_state()
                sleep(1)
                # gui.wait_until_prompted()
                (move, value) = opponent.action(game, True)
                game.take_action(move,value)
                gui.display_action()

        # gui.display_win()

    game.export_history("./pgns")  # save history


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Run a genetic algorithm.")
    parser.add_argument('-f', '--file', type=Path, default=Path('20240731_232634'), help="name of chromosome file")

    args = parser.parse_args()

    chromosome_path = Path("chromosomes") / f"{args.file}.json" 
    chromosome = Chromosome.from_file(chromosome_path)
    run_game(chromosome)

  
