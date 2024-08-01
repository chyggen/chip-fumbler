# This file creates a player vs agents game using the texasholdem GUI

# currently, the table has 6 players:
# - 1 user
# - 5 random agents


from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from agent import Agent
from chromosome import Chromosome


game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=2)
gui = TextGUI(game=game, visible_players=[0])

opponent = Agent(Chromosome(0.478, 0.565, 0.271, 0.621, 0.761, 0.904, 0.116, 0.22,  0.297, 0.668, 0.029))

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        if game.current_player == 0:
            gui.run_step()
        else:
            gui.display_state()
            game.take_action(opponent.action(game))
            gui.display_action()

    gui.display_win()

game.export_history("./pgns")  # save history

