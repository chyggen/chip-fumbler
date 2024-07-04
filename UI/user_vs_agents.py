# This file creates a player vs agents game using the texasholdem GUI 

# currently, the table has 6 players:
# - 1 user
# - 5 random agents


from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent

game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
gui = TextGUI(game=game,
              visible_players=[0])

while game.is_game_running():
    game.start_hand()

    while game.is_hand_running():
        if game.current_player == 0:
            gui.run_step()
        else:
            gui.display_state()
            game.take_action(*random_agent(game))
            gui.display_action()

    gui.display_win()

game.export_history('./pgns')     # save history