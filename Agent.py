import numpy as np
class Agent:
    
    def __init__(self):
        pass
    
    def play(self, state):
        actions = self.getActions(state)
        return best_action

    def setup(self):
        setup = np.chararray((3,8))
        setup[0,0] = 'F'
        setup[0,1] = 'B'
        setup[0,2] = '3'
        setup[0,3] = '3'
        setup[0,4] = '2'
        
        setup[1,0] = 'B'
        setup[1,1] = 'S'
        setup[1,2] = '2'
        setup[1,3] = '9'
        setup[1,4] = '10'
        return setup
