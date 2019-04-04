import numpy as np
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Concatenate, Input, Conv2D, Flatten
from copy import deepcopy
from keras.models import load_model

def one_hot(lst, size):
    return np.eye(size)[np.array([lst]).reshape(-1)]

'''
def one_hot_to_idx(one_hot_lst):
    print(np.where(one_hot_lst))
    return [ np.where(r==1)[0][0] for r in one_hot_lst[0] ]
'''

class TinyAgent:
    
    def __init__(self, is_random=True, is_p1 = True, model = None):
        self.is_random = is_random
        self.is_p1 = is_p1
        self.model = model
        
        self.prev_input   = [None, None] 
        #self.step_update  = 100
        #self.current_step = 0 
        
        self.discount = 0.9
        self.epsilon  = 1.0
        
        if not is_random:
            if self.model == None:
                
                '''
                self.input1 = Input(shape=(272,), name='board')
                self.x1 = Dense(10, activation='relu')(self.input1)
                self.input2 = Input(shape=(4,), name = 'action')
                self.x2 = Dense(10, activation='relu')(self.input2)
                self.conc = Concatenate()([self.x1, self.x2])                    # equivalent to added = keras.layers.add([x1, x2])
                self.out = Dense(1)(self.conc)
                self.model = Model(inputs = [self.input1, self.input2], outputs = self.out)
                self.model.compile(loss='mean_squared_error',
                                optimizer='adam')
                self.model.save('model.h5')
                '''
                
                
                self.input1   = Input(shape=(4,4,17), name='board')
                self.x1       = Conv2D(64, (2,2), strides=(1, 1))(self.input1)
                self.flat_x1  = Flatten()(self.x1)
                self.dense_x1 = Dense(10, activation='relu')(self.flat_x1)
                
                
                self.input2 = Input(shape=(4,), name = 'action')
                self.x2 = Dense(10, activation='relu')(self.input2)
                
                
                
                '''
                self.x1 = Dense(10, activation='relu')(self.input1)
                self.input2 = Input(shape=(4,), name = 'action')
                self.x2 = Dense(10, activation='relu')(self.input2)
                '''
                self.conc = Concatenate()([self.dense_x1, self.x2])                    # equivalent to added = keras.layers.add([x1, x2])
                self.out = Dense(1)(self.conc)
                self.model = Model(inputs = [self.input1, self.input2], outputs = self.out)
                self.model.compile(loss='mean_squared_error',
                                optimizer='adam')
                self.model.save('model.h5')
            
            #self.target_model = load_model('model.h5')
        
        
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
        
        # Random for random agent or epsilon greedy
        if self.is_random or np.random.random() < self.epsilon:
            #print(reward)
            return actions[np.random.randint(len(actions))]
         
        else:
            board = state[0]
            graveyards = state[1]
            graveyard_1 = graveyards[0]
            graveyard_2 = graveyards[1]
            
            
            
            # Transform the current board in one hot vector representation
            one_hot_board = self.transform_board(board)
            q_vals = np.zeros(len(actions))

            for i, action in enumerate(actions):
                action    = np.array(action)
                action    = action.flatten()
                #one_hot_board = one_hot_board.reshape((1,272))
                one_hot_board = one_hot_board.reshape((1,4,4,17))
                action        = action.reshape((1,4))
                q_vals[i]     = self.model.predict(x = [one_hot_board,  action], batch_size=1)[0]
            
            max_reward = np.max(q_vals)
        
        
        
            # Update previous action whenever there is one
            if(self.prev_input[0] is not None):
                q_target = reward + self.discount*max_reward
                #print(self.prev_input[0].shape)
                self.model.fit(x = [self.prev_input[0], np.array(self.prev_input[1]).flatten().reshape((1,4))], y = [q_target], batch_size = 1)
            
            # Set up current input to be the previous one
            #if len(actions) > 0:
            self.prev_input = [one_hot_board, actions[np.argmax(q_vals)]]
        
            print(self.prev_input[1])
            return actions[np.argmax(q_vals)]
    
    # Represent board as one hot vector
    def transform_board(self, board):
        one_hot_board = [[self.piece_dict[item] for item in row] for row in board]
        one_hot_board = [one_hot(row, len(self.piece_dict)) for row in one_hot_board]
        one_hot_board = np.array(one_hot_board)
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
        
        if(self.model is not None):
            q_target = reward
            #print(self.prev_input[1])
            self.model.fit(x = [self.prev_input[0], np.array(self.prev_input[1]).flatten().reshape((1,4))], y = [q_target])
            self.prev_input = [None, None]
