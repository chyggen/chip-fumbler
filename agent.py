from typing import Tuple, Optional
from math import exp
import random
import time
from pprint import pprint
import logging

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.game.hand_phase import HandPhase
from texasholdem.game.game import Pot
from texasholdem.game.game import Player
from chromosome import Chromosome
import FullHandProbability


def estimated_value (win_percentage, potSize, current_Bet):
    win_rate = win_percentage / 100
    loss_rate = (1-win_rate)
    win_pot = potSize 
    loss_pot = current_Bet
    ev = (win_rate * win_pot) - (loss_rate * loss_pot)     
    return ev

def perceived_win_percentage(tightness, hand_strength):
    if tightness == 0.5:
        return hand_strength
    else:
        gain = (tightness - 0.5) * abs(tightness - 0.5)
        mapping_numerator = 100 * (exp(gain*hand_strength) -1)
        mapping_denominator = exp(100*gain) - 1
        win_percent = mapping_numerator/mapping_denominator
        return win_percent

def is_bluffing(percentage):
    return random.random() < percentage

def want_to_raise(desired_raise: int, min_raise: int, max_raise: int, available_moves) -> Tuple[ActionType, Optional[int]]:
        
    # Desired raise is greater than our total chip amount
    if desired_raise >= max_raise and ActionType.RAISE in available_moves:
        logging.debug(f"tried to raise {desired_raise}, going ALL IN: {max_raise}")
        return (ActionType.ALL_IN, None)
        
    # Desired raise is less than our minimum possible raise
    elif desired_raise < min_raise or ActionType.RAISE not in available_moves:
        if ActionType.CALL in available_moves:
            logging.debug(f"cant raise {desired_raise}, CALLING")
            return (ActionType.CALL, None)
        elif ActionType.CHECK in available_moves:
            logging.debug(f"cant raise {desired_raise}, CHECKING")
            return (ActionType.CHECK, None)
        else: 
            raise RuntimeError("WTF cant call or check")
        
    # Desired raise is less than our total chip amount AND is more than our minimum possibile raise
    else:
        logging.debug(f"RAISING: {desired_raise}")
        return ActionType.RAISE, desired_raise
        # logging.debug("RAISE")
        # return (ActionType.RAISE, 100)

class Agent:

    # Create an agent based on a chromosome
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome
    
    # Decide the next move based on the game state and the agent's chromosome
    # Returns the action to take, plus a number of chips if the action is a raise
    def action(self, game: TexasHoldEm, debug: bool = True) -> Tuple[ActionType, Optional[int]]:

        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(filename = "test.log", level=log_level, format='\n %(message)s')
        #time.sleep(1)

        # game_phase is the stage of the game (PREFLOP, FLOP, TURN, RIVER)
        game_phase = game.hand_phase
        potSize = game.pots[0].get_total_amount()
        logging.debug(potSize)
        raiseAction = 0

        logging.debug('\n\n\n')

        # logging.debug(vars(game))

        logging.debug(f'CURRENT GAME PHASE: {game_phase}')
        logging.debug(f"PLAYER {game.current_player}'s TURN")
        logging.debug(f"HAND {game.get_hand(game.current_player)}")
        logging.debug(f"BOARD {game.board}")
        logging.debug(f"AVAILABLE MOVES {game.get_available_moves()}")
        
        # game.get_hand(game.current_player)
        # hand[0], hand[1]
        
        hand_strength: float
        aggressiveness: float
        bluff_probability: float
        tightness: float
        
        # # Parameters from agent's chromosome
        # aggressiveness_preflop = self.chromosome.aggressiveness_preflop   
        # aggressiveness_flop = self.chromosome.aggressiveness_flop
        # aggressiveness_turn = self.chromosome.aggressivenss_trun
        # aggressiveness_river = self.chromosome.aggressivness_river
        # bluff_probability_preflop = self.chromosome.bluff_probability_preflop
        # bluff_probability_flop = self.chromosome.bluff_probability_flop
        # bluff_probability_turn = self.chromosome.bluff_probability_turn
        # bluff_probability_river = self.chromosome.bluff_probability_river
        # tightness_vs_looseness = self.chromosome.tightness_vs_looseness
        # dynamic_vs_static = self.chromosome.dynamic_vs_static
        
        # logging.debug(self.chromosome)

        # Extracting parameters based on the current game phase
        aggressiveness = {
            HandPhase.PREFLOP: self.chromosome.aggressiveness_preflop,
            HandPhase.FLOP: self.chromosome.aggressiveness_flop,
            HandPhase.TURN: self.chromosome.aggressiveness_turn,
            HandPhase.RIVER: self.chromosome.aggressiveness_river,
        }[game_phase]
        
        bluff_probability = {
            HandPhase.PREFLOP: self.chromosome.bluff_probability_preflop,
            HandPhase.FLOP: self.chromosome.bluff_probability_flop,
            HandPhase.TURN: self.chromosome.bluff_probability_turn,
            HandPhase.RIVER: self.chromosome.bluff_probability_river,
        }[game_phase]

        tightness = self.chromosome.tightness_vs_looseness
        #tightness = 0.5

        # Get player's chip size
        #game.current_player
        
        chipSize = game.players[game.current_player].chips
        
        # Evaluate hand strength
        if game_phase == HandPhase.PREFLOP:
            hand_strength = FullHandProbability.preflop_evaluate_hand_strength(game.get_hand(game.current_player))
        else:
            hand_strength = FullHandProbability.after_preflop_hand_strength_prob(game.board, game.get_hand(game.current_player))        
    
        # Calculate perceived win percentage
        win_percentage = perceived_win_percentage(tightness, hand_strength)

        # Amount to lose
        to_lose = game.chips_to_call(game.current_player)
        
        EV1 = estimated_value(win_percentage, potSize, to_lose)

        logging.debug(f'Total chip size size: {chipSize}')
        logging.debug(f'HAND STRENGTH: {hand_strength}')
        logging.debug(f'PERCEIVED WIN%: {win_percentage}')
        logging.debug(f"POT SIZE: {potSize}")
        logging.debug(f"POTS : {game.pots}")
        logging.debug(f"MIN RAISE: {game.min_raise()}")
        logging.debug(f'TO LOSE: {to_lose}')
        logging.debug(f'EV1: {EV1}')
        
    
        
        move: Tuple[ActionType, Optional[int]]

        if EV1 <= 0: 
            """BAD HAND"""    
            #This checks if we are bluffing.
            if is_bluffing(bluff_probability):
                """WE ARE BLUFFING"""
                raise_val_bluff = 20 

                # Check if the current phase is PREFLOP and handle the edge case
                if game_phase == HandPhase.PREFLOP:
                    if ActionType.CALL in game.get_available_moves():
                        logging.debug("Edge Case PREFLOP: Calling instead of raising")
                        move = (ActionType.CALL, None)

                    elif ActionType.CHECK in game.get_available_moves():
                        logging.debug("Edge Case PREFLOP: Checking instead of raising")
                        move = (ActionType.CHECK, None)

                    else:
                        logging.debug("Edge Case PREFLOP: Folding")
                        move = (ActionType.FOLD, None)

                else:
                    move = want_to_raise(raise_val_bluff, game.min_raise(), chipSize, game.get_available_moves())

            else:
                """WE ARE NOT BLUFFING"""
                # In the event that the player does not want to bluff, check/fold.
                if ActionType.CHECK in game.get_available_moves():
                    logging.debug("CHECKING")
                    move = (ActionType.CHECK, None)

                else:
                    #logging.debug("FOLDING")
                    move = (ActionType.FOLD, None)

        
        else:
            """GOOD HAND"""
            # Positive EV value
            new_lose = (2 / 3) * potSize
            # if new_lose >= chipSize:
            #     logging.debug(f"ALL IN {chipSize}")
            #     move = (ActionType.ALL_IN, None)
            # else:
            EV2 = estimated_value(win_percentage, potSize, new_lose)
            logging.debug(f"EV2: {EV2}")

            EV2_with_aggressiveness = EV2 * (2 * aggressiveness)

            if EV2_with_aggressiveness < 0:
                if ActionType.CHECK in game.get_available_moves():
                    logging.debug("CHECKING")
                    move = (ActionType.CHECK, None)

                else:
                    logging.debug(f"CALLING")
                    move = (ActionType.CALL, None)

            else:
                if EV2_with_aggressiveness <= 2:
                    raiseAction = int(potSize * 2)
                elif 2 < EV2_with_aggressiveness <= 5:
                    raiseAction = int(potSize * 3)
                elif EV2_with_aggressiveness > 10:
                    raiseAction = int(potSize * 4)
                
                # Check if the current phase is PREFLOP and handle the edge case
                if game_phase == HandPhase.PREFLOP:
                    if ActionType.CALL in game.get_available_moves():
                        logging.debug("Edge Case PREFLOP: Calling instead of raising")
                        move = (ActionType.CALL, None)

                    elif ActionType.CHECK in game.get_available_moves():
                        logging.debug("Edge Case PREFLOP: Checking instead of raising")
                        move = (ActionType.CHECK, None)

                    else:
                        logging.debug("Edge Case PREFLOP: Folding")
                        move = (ActionType.FOLD, None)

                else:
                    move = want_to_raise(raiseAction, game.min_raise(), chipSize, game.get_available_moves())
                    
        logging.debug(f"move: {move}, type: {type(move)}")
        logging.debug(f"valid? {game.validate_move(game.current_player, move)}")
        # if not game.validate_move(game.current_player, move):
        # print(f"WARNING: {move} is not a valid move, options are {game.get_available_moves()}")

        return move

            # if raiseAction > chipSize:
            #     logging.debug(f"going all in with {chipSize} chips, tried to raise {raiseAction} ")
            #     logging.debug(f"ALL IN {chipSize}")
            #     return ActionType.ALL_IN
            
            # if raiseAction < game.min_raise():
            #     if (ActionType.CHECK in game.get_available_moves()):
            #         logging.debug("CHECKING")
            #         return ActionType.CHECK
            #     else:
            #         logging.debug("CALLING")
            #         return ActionType.CALL
                    
            
            # game.min_raise()
            # game.chips_to_call(game.current_player)

            # logging.debug(f'RAISING WITH: {raiseAction}')

            # return (ActionType.RAISE, raiseAction)


    # Get the agent's underlying chromosome
    def get_chromosome(self) -> Chromosome:
        return self.chromosome



# A child class that makes random moves, used for testing
class RandomAgent:
    def __init__(self, id):
        # since random agents do not have a chromosome, they need an ID to be 
        # differentiable from other random agents
        self.id = id
        pass

    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        return random_agent(game)

    def get_chromosome(self) -> None:
        return None
