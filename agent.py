from typing import Tuple, Optional

from texasholdem.game.game import TexasHoldEm
from texasholdem.game.action_type import ActionType
from texasholdem.agents.basic import random_agent
from texasholdem.game.hand_phase import HandPhase
from texasholdem.game.action_type import ActionType
from chromosome import Chromosome


class Agent:

    # Create an agent based on a chromosome
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome

    # Decide the next move based on the game state and the agent's chromosome
    # Returns the action to take, plus a number of chips if the action is a raise
    def action(self, game: TexasHoldEm) -> Tuple[ActionType, Optional[int]]:
        x1 = 40#from trained bot persentage for flop
        x2 = 50#for per flop
        x3 = 50#for perhand
        x4 = 50#for river
        y1 = 60#perobablity of wining for flop
        y2 = 60#for per flop
        y3 = 60#for perhand
        y4 = 60#for river
        raiseAction = 0
        potSize = 5000
        chipSize = 1000
        
        #game state 
        if game.hand_phase == HandPhase.FLOP:
            if x1 < y1 <= 75 :
                #do math based on pot size and persetage to call
               return  'CHECK'
            if 75 < y1 <= 100 :
                #do math based on pot size 
                raiseAction = potSize/chipSize*2 # temp will need to be changed 
                return 'RAISE {raiseAction}'
            else:
                return 'FOLD' 
            
        if game.hand_phase == HandPhase.PREFLOP:
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
