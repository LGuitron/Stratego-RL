import numpy as np
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Concatenate, Input

def one_hot(lst, size):
    return np.eye(size)[np.array([lst]).reshape(-1)]

'''
def one_hot_to_idx(one_hot_lst):
    print(np.where(one_hot_lst))
    return [ np.where(r==1)[0][0] for r in one_hot_lst[0] ]
'''

class TinyAgent:
    
    def __init__(self, is_random=True, is_p1 = True):
        self.is_random = is_random
        self.is_p1 = is_p1
        self.state_model = Sequential()
        self.state_model.add(Dense(32, input_shape=(68,1)))
        self.state_model.add(Dense(16))
        self.state_model.add(Dense(1))
        
        self.input1 = Input(shape=(272,), name='board')
        self.x1 = Dense(10, activation='relu')(self.input1)
        self.input2 = Input(shape=(4,), name = 'action')
        self.x2 = Dense(10, activation='relu')(self.input2)
        self.conc = Concatenate()([self.x1, self.x2])                    # equivalent to added = keras.layers.add([x1, x2])
        self.out = Dense(1)(self.conc)
        self.model = Model(inputs = [self.input1, self.input2], outputs = self.out)
        self.model.compile(loss='mean_squared_error',
                           optimizer='adam')
        
        self.piece_dict =       {   0    : 0, 
                                    1    : 1,
                                    2    : 2,
                                    3    : 3,
                                    9    : 4,
                                    10   : 5,
                                    99   : 6,
                                    101  : 7,
                                    -102 : 8,
                                    103  : 9,
                                    -1   : 10,
                                    -2   : 11,
                                    -3   : 12,
                                    -9   : 13,
                                    -10  : 14,
                                    -99  : 15,
                                    -101 : 16
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
        board = state[0]
        graveyards = state[1]
        graveyard_1 = graveyards[0]
        graveyard_2 = graveyards[1]
        
        
        
        # Transform the current board in one hot vector representation
        one_hot_board = self.transform_board(board)
        q_vals = []
        
        inputs = []
        for action in actions:
            action    = np.array(action)
            action    = action.flatten()
            print(one_hot_board.shape)
            #input_var = np.array([one_hot_board, action])
            #input_var = input_var.reshape((1,2))
            #print(input_var.shape)
            q_vals.append(self.model.predict({'board' : one_hot_board, 'action' : action}))
            
            
            #inputs.append(input_var)
            #inputs = np.array(inputs)
    
        #q_vals = self.model.predict(inputs)

        print(q_vals)
        exit()
        
        if self.is_random:
            #print(reward)
            return actions[np.random.randint(len(actions))]
         
        else:
            pass
    
    # Represent board as one hot vector
    def transform_board(self, board):
        one_hot_board = [[self.piece_dict[item] for item in row] for row in board]
        one_hot_board = [one_hot(row, len(self.piece_dict)) for row in one_hot_board]
        one_hot_board = np.array(one_hot_board)
        one_hot_board = one_hot_board.flatten()
        return np.array(one_hot_board)

    def setup(self, pieces, setup_area):
        setup = np.zeros(setup_area)
    
        if(self.is_p1):
            setup[0][0] = pieces[9]
            setup[1][0] = pieces[8]
            setup[0][3] = pieces[3]
        
        else:
            setup[1][0] = pieces[9]
            setup[0][0] = pieces[8]
            setup[1][1] = pieces[2]
        
        
        return setup

    # Receive reward for winning or losing the game
    def receive_last_reward(self, reward):
        pass
        #print(reward)
        
        
        
        
        
        

