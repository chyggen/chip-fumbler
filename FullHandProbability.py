# This file creates a player vs agents game using the texasholdem GUI

# currently, the table has 6 players:
# - 1 user
# - 5 random agents


from texasholdem.game.game import TexasHoldEm
#from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents.basic import random_agent
from texasholdem.game.hand_phase import HandPhase 
from texasholdem import Card
from texasholdem.evaluator import evaluate, rank_to_string, get_five_card_rank_percentage
import random

#game = TexasHoldEm(buyin=500, big_blind=5, small_blind=2, max_players=6)
#gui = TextGUI(game=game, visible_players=[0])



def after_preflop_hand_strength_prob(board_cards, hand):
    # Get the current board (community) cards
    #board_cards = game.board
    board_hand_cards = [Card(str(card)) for card in board_cards]

    # Evaluate the player's hand using the community cards
    hand_rank = evaluate(cards=hand, board=board_hand_cards)
    hand_rank_str = rank_to_string(hand_rank)

    # Calculate hand strength probability
    hand_strength_prob = 100 * get_five_card_rank_percentage(hand_rank)
    return hand_strength_prob


#This will calculate the preflop hand strength based on the number given by this website https://www.raketherake.com/news/2023/05/win-percentage-of-every-poker-starting-hands
def preflop_evaluate_hand_strength(hand):
    """Returns an estimated win rate percentage for the given hand."""
    precomputed_win_rates = {

        #This is for the Pairs.
        ('A', 'A', True): 84.9, ('K', 'K', True): 73.2, ('Q', 'Q', True): 79.6,
        ('J', 'J', True): 77.1, ('T', 'T', True): 74.7, ('9', '9', True): 71.7,
        ('8', '8', True): 68.7, ('7', '7', True): 65.7, ('6', '6', True): 62.7,
        ('5', '5', True): 59.6, ('4', '4', True): 56.3, ('3', '3', True): 52.9,
        ('2', '2', True): 49.3, 
        
        #This is for the Ace high suited hands
        ('A', 'K', True): 66.2, ('A', 'Q', True): 65.5, ('A', 'J', True): 64.0, 
        ('A', '9', True): 60.0, ('A', '8', True): 58.9, ('A', '7', True): 57.7,
        ('A', '6', True): 56.4, ('A', '5', True): 56.3, ('A', '4', True): 55.3,
        ('A', '3', True): 54.5, ('A', '2', True): 53.6,

        #This is for the King high suited hands
        ('K', 'Q', True): 62.4, ('K', 'J', True): 59.9, ('K', 'T', True): 59.0, 
        ('K', '9', True): 57.0, ('K', '8', True): 55.0, ('K', '7', True): 54.0, 
        ('K', '6', True): 52.9, ('K', '5', True): 51.9, ('K', '4', True): 50.9, 
        ('K', '3', True): 50.0, ('K', '2', True): 49.1,

        #This is for the Queen high suited hands
        ('Q', 'J', True): 59.1, ('Q', 'T', True): 56.5, ('Q', '9', True): 54.5,
        ('Q', '8', True): 52.6, ('Q', '7', True): 50.5, ('Q', '6', True): 49.7,
        ('Q', '5', True): 48.6, ('Q', '4', True): 47.7, ('Q', '3', True): 46.8,
        ('Q', '2', True): 45.9,
        
        #This is for the Jack high suited hands
        ('J', 'T', True): 56.2, ('J', '9', True): 52.3, ('J', '8', True): 50.4,
        ('J', '7', True): 48.4, ('J', '6', True): 46.4, ('J', '5', True): 45.6,
        ('J', '4', True): 44.6, ('J', '3', True): 43.8, ('J', '2', True): 42.8, 
        
        #This is for the Ten high suited hands
        ('T', '9', True): 52.4, ('T', '8', True): 48.5, ('T', '7', True): 46.5,
        ('T', '6', True): 44.6, ('T', '5', True): 42.6, ('T', '4', True): 41.8,
        ('T', '3', True): 40.9, ('T', '2', True): 40.1,

        #This is for the Nine high suited hands
        ('9', '8', True): 48.9, ('9', '7', True): 44.8, ('9', '6', True): 42.9,
        ('9', '5', True): 40.9, ('9', '4', True): 38.9, ('9', '3', True): 38.3,
        ('9', '2', True): 37.4,

        #This is for the Eight high suited hands 
        ('8', '7', True): 45.7, ('8', '6', True): 41.5, ('8', '5', True): 39.6,
        ('8', '4', True): 37.5, ('8', '3', True): 35.6, ('8', '2', True): 35.0,

        #This is for the Seven high suited hands
        ('7', '6', True): 42.9, ('7', '5', True): 38.5, ('7', '4', True): 36.5,
        ('7', '3', True): 34.6, ('7', '2', True): 32.6,

        #This is for the Six high suited hands
        ('6', '5', True): 40.3, ('6', '4', True): 35.9, ('6', '3', True): 34.0,
        ('6', '2', True): 32.0,

        #This is for the Five high suited hands
        ('5', '4', True): 38.5, ('5', '3', True): 34.0, ('5', '2', True): 32.1, 
        
        #This is for the Four high suited hands
        ('4', '3', True): 35.7, ('4', '2', True): 31.10,

        #This is for the Three high sutied hand
        ('3', '2', True): 33.1,

        #For the pairs again.
        ('A', 'A', False): 84.9, ('K', 'K', False): 73.2, ('Q', 'Q', False): 79.6,
        ('J', 'J', False): 77.1, ('T', 'T', False): 74.7, ('9', '9', False): 71.7,
        ('8', '8', False): 68.7, ('7', '7', False): 65.7, ('6', '6', False): 62.7,
        ('5', '5', False): 59.6, ('4', '4', False): 56.3, ('3', '3', False): 52.9,
        ('2', '2', False): 49.3, 
        

        ('A', 'K', False): 64.5, ('A', 'Q', False): 65.5,
        ('A', 'J', False): 64.0, ('K', 'Q', False): 60.5, ('K', 'J', False): 59.9,
        ('Q', 'J', False): 57.0, ('J', 'T', False): 53.8, ('T', '9', False): 49.8,
        ('9', '8', False): 46.1, ('8', '7', False): 42.7, ('7', '6', False): 39.7,
        ('6', '5', False): 37.0, ('5', '4', False): 35.1, ('4', '3', False): 32.1,
        ('3', '2', True): 29.3,
        # Add more as needed
    }

    rank_map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
        '7': 7, '8': 8, '9': 9, 'T': 10, 
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    ranks = [Card.INT_RANKS.index(card >> 8 & 0xF) for card in hand]
    suited = (hand[0] >> 12 & 0xF) == (hand[1] >> 12 & 0xF)
    #print(f'Hand: {hand[0]}, {hand[1]}')
    ranks.sort(reverse=True)

    hand_key = (Card.STR_RANKS[ranks[0]], Card.STR_RANKS[ranks[1]], suited)
    win_rate = precomputed_win_rates.get(hand_key, 35.0)  # Default to 35% for unlisted hands

    return win_rate


# while game.is_game_running():
#     game.start_hand()

#     player_hand = game.get_hand(0)  # This takes the hand of Agent 0 or the players hand.
#     #print(f"Your hand: {player_hand}")

#     test_hand = [Card(str(card)) for card in player_hand]
#     print(f"Your hand: {test_hand}")

    
#     win_rate = preflop_evaluate_hand_strength(test_hand)
#     print(f"Estimated win rate for your preflop hand: {win_rate:.2f}%")


#     while game.is_hand_running():

#         if game.current_player == 0:

#             #This checks for the current hand phase
#             if game.hand_phase == HandPhase.FLOP:

#                 #Take the 3 cards(flop cards) from the board.
#                 flop_cards = game.board[:3]
#                 flop_cards2 = [Card(str(card)) for card in flop_cards] 
#                 print(f"Flop Cards: {flop_cards2}")

#                 board_cards = game.board
#                 board_hand_cards = [Card(str(card)) for card in board_cards]

#                 # Evaluate the player's hand using the community cards
#                 hand_rank = evaluate(cards=test_hand, board=board_hand_cards)
#                 hand_rank_str = rank_to_string(hand_rank)

#                 # Calculate hand strength probability
#                 hand_strength_prob = get_five_card_rank_percentage(hand_rank)
                
#                 # Display the hand rank and strength probability
#                 print(f"Your hand: {test_hand} | Board: {board_cards}")
#                 print(f"Hand evaluation: {hand_rank_str}")
#                 print(f"PreFlop Hand strength probability: {hand_strength_prob:.2%}")

#             elif game.hand_phase in [HandPhase.TURN, HandPhase.RIVER, HandPhase.SETTLE]:
#                 # Get the current board (community) cards
#                 board_cards = game.board
#                 board_hand_cards = [Card(str(card)) for card in board_cards]

#                 # Evaluate the player's hand using the community cards
#                 hand_rank = evaluate(cards=test_hand, board=board_hand_cards)
#                 hand_rank_str = rank_to_string(hand_rank)

#                 # Calculate hand strength probability
#                 hand_strength_prob = get_five_card_rank_percentage(hand_rank)
                
#                 # Display the hand rank and strength probability
#                 print(f"Your hand: {test_hand} | Board: {board_cards}")
#                 print(f"Hand evaluation: {hand_rank_str}")
#                 print(f"Hand strength probability: {hand_strength_prob:.2%}")

#             # gui.run_step()
#         else:
#             # gui.display_state()
#             game.take_action(*random_agent(game))
#             # gui.display_action()

#     # gui.display_win()