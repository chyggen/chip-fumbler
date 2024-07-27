from typing import Tuple, Optional
from math import exp
import random

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.game.hand_phase import HandPhase
from texasholdem.game.action_type import ActionType
from texasholdem.game.game import Pot
from texasholdem.game.game import Player
from chromosome import Chromosome
import FullHandProbability

def estimated_value (win_percentage, potSize, current_Bet):
    loss_percentage = (1-win_percentage)
    win_pot = potSize 
    loss_pot = current_Bet
    ev = (win_percentage*win_pot) - (loss_percentage*loss_pot)     
    return ev

def perceived_win_percentage(tightness, hand_strength):
    gain = (tightness - 0.5) * abs(tightness - 0.5)
    mapping_numerator = 100 * (exp(gain*hand_strength) -1)
    mapping_denominator = exp(100*gain) - 1
    win_percent = mapping_numerator/mapping_denominator
    return win_percent

def is_bluffing(percentage):
    return random.random < percentage

class Agent:

    # Create an agent based on a chromosome
    def __init__(self, player_id: int, chromosome: Chromosome):
        self.player_id = player_id
        self.chromosome = chromosome
    
    # Decide the next move based on the game state and the agent's chromosome
    # Returns the action to take, plus a number of chips if the action is a raise
    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:

        # game_phase is the stage of the game (PREFLOP, FLOP, TURN, RIVER)
        game_phase = game.hand_phase
        potSize = Pot.get_total_amount # totol pot size
        raiseAction = 0
        
        hand_strength: float
        aggressiveness: float
        bluff_prob: float
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
        
        # print(self.chromosome)

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

        # Get player's chip size
        #game.current_player
        
        chipSize = game.pots[0].get_player_amount(self.player_id)
        print(chipSize)
        
        # Evaluate hand strength
        if game_phase == HandPhase.PREFLOP:
            hand_strength = FullHandProbability.preflop_evaluate_hand_strength(game.get_hand(game.current_player))
        else:
            hand_strength = FullHandProbability.after_preflop_hand_strength_prob(game.board, game.get_hand(game.current_player))
        
        # Calculate perceived win percentage
        win_percentage = perceived_win_percentage(tightness, hand_strength)

        # Amount to lose
        to_lose = game.last_raise
        EV1 = estimated_value(win_percentage, potSize, to_lose)
    
        """BAD HAND"""
        if EV1 <= 0:     
            #This checks if we are bluffing.
            if is_bluffing(bluff_probability):
                """WE ARE BLUFFING"""
                # TODO add bluffing aggressiveness
                # bluff_aggressiveness: float
                raise_val_bluff = (2/3)*potSize 

                #This checks if the raise value for the bluff is bigger than the players chipSize
                if(raise_val_bluff >= chipSize):
                    return ActionType.ALL_IN
                else:
                    return (ActionType.RAISE, raise_val_bluff)
            else:
                """WE ARE NOT BLUFFING"""
                #In the event that the player does not want to bluff check/fold.
                if (ActionType.CHECK in list(game.get_available_moves())):
                    return ActionType.CHECK
                else:
                    return ActionType.FOLD
        
        """GOOD HAND"""
        # Positive EV value
        new_lose = (2 / 3) * potSize
        if new_lose >= chipSize:
            return ActionType.ALL_IN
        else:
            EV2 = estimated_value(win_percentage, potSize, new_lose)
            EV2_with_aggressiveness = EV2 * (2 * aggressiveness)

            if 0 < EV2_with_aggressiveness <= 25:
                raiseAction = (potSize / chipSize) * 2
                return (ActionType.RAISE, raiseAction)
            elif 25 < EV2_with_aggressiveness <= 50:
                raiseAction = (potSize / chipSize) * 3
                return (ActionType.RAISE, raiseAction)
            elif EV2_with_aggressiveness > 50:
                raiseAction = (potSize / chipSize) * 4
                return (ActionType.RAISE, raiseAction)

###########################################################################################################################################################################################################
        # #game state 
        # if game.hand_phase == HandPhase.PREFLOP:
        #     if game.last_raise == 0:#if it has not been rased 
        #         if 50 < propertyOfWin <= 75 :
        #         #do math based on pot size and persetage to call
        #             return  ActionType.CHECK
        #         if 75 < propertyOfWin <= 100 :#do math based on pot size 
        #             raiseAction = potSize/chipSize*agesovesThreshold # temp will need to be changed 
        #             return (ActionType.RAISE, raiseAction)
        #         else:
        #             return ActionType.FOLD 
        #     else:
        #         if agesovesThreshold < propertyOfWin <= 75 :
        #         #do math based on pot size and persetage to call
        #             return ActionType.CALL 
        #         if 75 < propertyOfWin <= 100 :
        #             #do math based on pot size 
        #             #if raiseAction > callamouin
        #             raiseAction = potSize/chipSize*2 # temp will need to be changed change to call amount 
        #             return (ActionType.RAISE, raiseAction)
        #         else:
        #             return ActionType.FOLD 
        


        # ##################
        # """PREFLOP STAGE""" 
        # ##################
        # if game.hand_phase == HandPhase.PREFLOP:
        #     #This evaluates for the hand strength of the hand on the preflop.
        #     hand_strength = FullHandProbability.preflop_evaluate_hand_strength(game.get_hand(game.current_player))
        #     #TODO Make the perceived win percentage function.
        #     win_percentage = perceived_win_percentage(tightness, hand_strength)  
            
        #     #math
        #     to_lose = game.last_raise# will need to be changed we dont know how to get are possible bet to lose 
        #     EV1 = estimated_value(win_percentage, potSize, to_lose)
            
        #     #This is for a bad hand.
        #     if (EV1 <= 0):     
        #         bluffing = is_bluffing(bluff_from_chromosome_value)
        #         #This checks if we are bluffing.
        #         if(bluffing):
        #             # TODO add bluffing aggressiveness
        #             # bluff_aggressiveness: float
        #             raise_val_bluff = (2/3)*potSize 

        #             #This checks if the raise value for the bluff is bigger than the players chipSize
        #             if(raise_val_bluff >= chipSize):
        #                 return ActionType.ALL_IN
        #             else:
        #                 return (ActionType.RAISE, raise_val_bluff)
        #         else:
        #             #In the event that the player does not want to bluff check/fold.
        #             if (ActionType.CHECK in list(game.get_available_moves())):
        #                 return ActionType.CHECK
        #             else if (ActionType.CALL in list(game.get_avalable_moves()))
        #             else:
        #                 return ActionType.FOLD
                
            # math for positive ev value
                    #betting amount math        
            
            # #####################################################            
            # new_lose = (2/3)*potSize #CHANGE THIS LATER
            # if (new_lose >= chipSize):#if we dont have enough chips then all in baby 
            #     return (ActionType.ALL_IN)        
            # else:
            #     EV2 = estimated_value(win_percentage, potSize, new_lose)
            #     EV2_with_aggressiveness = EV2 * (2 * aggressiveness) 
                
            #     if (0 < EV2_with_aggressiveness <= 25):
            #         raiseAction = (potSize / chipSize) *2
            #         return (ActionType.RAISE, raiseAction)
            #     elif (25 < EV2_with_aggressiveness <= 50):
            #         raiseAction = (potSize / chipSize) *3 
            #         return (ActionType.RAISE, raiseAction)
            #     elif (EV2_with_aggressiveness > 50 ):
            #         raiseAction = (potSize / chipSize) *4 
            #         return (ActionType.RAISE, raiseAction)
            
            
        

        # ##################
        # """FLOP STAGE"""
        # ##################
        # if game.hand_phase == HandPhase.FLOP:

        #     #pull matts value 
        #     if x2 < y2 <= 75 :
        #         #do math based on pot size and persetage to call
        #        return  call/check
        #     if 75 < y2 <= 100 :
        #         #do math based on pot size 
        #         raiseAction = potSize/chipSize*2 # temp will need to be changed 
        #         return 'RAISE {raiseAction}'
        #     else:
        #         return 'FOLD' 
               
        # ##################
        # """TURN STAGE"""
        # ##################
        # if game.hand_phase == HandPhase.TURN:
        #     if x3 < y3 <= 75 :
        #         #do math based on pot size and persetage to call
        #        return  call/check
        #     if 75 < y3 <= 100 :
        #         #do math based on pot size 
        #         raiseAction = potSize/chipSize*2 # temp will need to be changed 
        #         return 'RAISE {raiseAction}'
        #     else:
        #         return 'FOLD' 
            
        # ##################
        # """RIVER STAGE"""
        # ##################
        # if game.hand_phase == HandPhase.RIVER:
        #     if 75 < y4 <= 100 : 
        #         #do math based on pot size 
        #         raiseAction = potSize/chipSize*2 # temp will need to be changed 
        #         return 'RAISE {raiseAction}'
        #     else:
        #         return 'FOLD'        
       
       ###############################################################################################################################################################################


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
