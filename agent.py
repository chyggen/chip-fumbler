from typing import Tuple, Optional

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.game.hand_phase import HandPhase
from texasholdem.game.action_type import ActionType
from texasholdem.game.game import Pot
from chromosome import Chromosome


class Agent:

    # Create an agent based on a chromosome
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome

    # Decide the next move based on the game state and the agent's chromosome
    # Returns the action to take, plus a number of chips if the action is a raise
    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        agesovesThreshold = Chromosome.aggressiveness_preflop#from trained bot persentage for flop
        x2 = 50#for per flop
        x3 = 50#for perhand
        x4 = 50#for river
        propertyOfWin = 60#perobablity of wining for flop
        y2 = 60#for per flop
        y3 = 60#for perhand
        y4 = 60#for river
        raiseAction = 0
        potSize = Pot.amount # totol pot size
        for i in player_id_array :
            chipSize = Pot.get_player_amount(i)
        
        #game state 
        if game.hand_phase == HandPhase.PREFLOP:
            if game.last_raise == 0:#if it has not been rased 
                if 50 < propertyOfWin <= 75 :
                #do math based on pot size and persetage to call
                    return  ActionType.CHECK
                if 75 < propertyOfWin <= 100 :#do math based on pot size 
                    raiseAction = potSize/chipSize*agesovesThreshold # temp will need to be changed 
                    return (ActionType.RAISE, raiseAction)
                else:
                    return ActionType.FOLD 
            else:
                if agesovesThreshold < propertyOfWin <= 75 :
                #do math based on pot size and persetage to call
                    return ActionType.CALL 
                if 75 < propertyOfWin <= 100 :
                    #do math based on pot size 
                    #if raiseAction > callamouin
                    raiseAction = potSize/chipSize*2 # temp will need to be changed change to call amount 
                    return (ActionType.RAISE, raiseAction)
                else:
                    return ActionType.FOLD 
            
        if game.hand_phase == HandPhase.FLOP:
            #pull matts value 
            if x2 < y2 <= 75 :
                #do math based on pot size and persetage to call
               return  call/check
            if 75 < y2 <= 100 :
                #do math based on pot size 
                raiseAction = potSize/chipSize*2 # temp will need to be changed 
                return 'RAISE {raiseAction}'
            else:
                return 'FOLD' 
               
        if game.hand_phase == HandPhase.PREHAND:
            if x3 < y3 <= 75 :
                #do math based on pot size and persetage to call
               return  call/check
            if 75 < y3 <= 100 :
                #do math based on pot size 
                raiseAction = potSize/chipSize*2 # temp will need to be changed 
                return 'RAISE {raiseAction}'
            else:
                return 'FOLD' 
            
        if game.hand_phase == HandPhase.RIVER:
            if x4 < y4 <= 75 :
                #do math based on pot size and persetage to call
               return  call/check
            if 75 < y4 <= 100 :
                #do math based on pot size 
                raiseAction = potSize/chipSize*2 # temp will need to be changed 
                return 'RAISE {raiseAction}'
            else:
                return 'FOLD'           

    # Get the agent's underlying chromosome
    def get_chromosome(self) -> Chromosome:
        return self.chromosome


# A child class that makes random moves, used for testing
class RandomAgent(Agent):
    def __init__(self, id):
        # since random agents do not have a chromosome, they need an ID to be 
        # differentiable from other random agents
        self.id = id
        pass

    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        return random_agent(game)

    def get_chromosome(self) -> None:
        return None
