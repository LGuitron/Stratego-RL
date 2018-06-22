import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense


def one_hot(lst, size):
    return np.eye(size)[np.array([lst]).reshape(-1)]


def one_hot_to_idx(one_hot_lst):
    print(np.where(one_hot_lst))
    return [ np.where(r==1)[0][0] for r in one_hot_lst[0] ]


class Agent:
    
    def __init__(self, is_random=True, is_p1 = True):
        self.is_random = is_random
        self.is_p1 = is_p1
        self.raw_model = Sequential()
        self.raw_model.add(Dense(32, input_shape=(68,1)))
        self.raw_model.add(Dense(16))
        self.raw_model.add(Dense(1))
        
        self.piece_dict = {    0   : {"movable": False, "print":'  -  '},
                                    1   : {"movable": True,  "print":'  S  ', "grave_index":0},
                                    2   : {"movable": True,  "print":'  2  ', "grave_index":1, "long_move" : None},
                                    3   : {"movable": True,  "print":'  3  ', "grave_index":2},  
                                    9   : {"movable": True,  "print":'  9  ', "grave_index":3},  
                                    10  : {"movable": True,  "print":'  10 ', "grave_index":4}, 
                                    99  : {"movable": False, "print":'  B  ', "grave_index":5},
                                    101 : {"movable": False, "print":'  F  ', "grave_index":6},
                                    self.unknown_key : {"movable": False, "print":'  U  '},
                                    self.impassable  : {"movable": False, "print":'  X  '}
                                }
    
    def play(self, state, actions, reward):
        #
        # Inputs
        #
        #
        # state: current board
        #
        # actions: List of tuples that represent possible actions
        #
        # reward: Reward from last action
        if self.is_random:
            return actions[np.random.randint(len(actions))]
            
            
        else:
            pass
    
    
    

    def setup(self, pieces, setup_area):
        setup = np.zeros(setup_area)
    
        if(self.is_p1):
            setup[0][0] = pieces[9]
            setup[0][1] = pieces[8]
            setup[0][2] = pieces[3]
            setup[0][3] = pieces[2]
            setup[0][4] = pieces[0]
            
            setup[1][0] = pieces[7]
            setup[1][1] = pieces[6]
            setup[2][3] = pieces[1]
            setup[1][3] = pieces[4]
            setup[1][4] = pieces[5]
        
        else:
            setup[2][0] = pieces[9]
            setup[2][1] = pieces[8]
            setup[2][2] = pieces[3]
            setup[2][3] = pieces[2]
            setup[2][4] = pieces[0]
            
            setup[1][0] = pieces[7]
            setup[1][1] = pieces[6]
            setup[0][3] = pieces[1]
            setup[1][3] = pieces[4]
            setup[1][4] = pieces[5]
        
        
        return setup

    # Receive reward for winning or losing the game
    def receive_last_reward(self, reward):
        pass
        #print(reward)
        
        
        
        
        
        

