import numpy as np
from copy import deepcopy
from Agent import Agent
class Environment:
    
    def __init__(self, p1, p2):
        self.board          = np.chararray((8,8))
        self.board_p1       = np.zeros((8,8,17)) 
        self.board_p2       = np.zeros((8,8,17))
        self.prev_board_p1  = None
        self.prev_board_p2  = None
        self.p1             = p1
        self.p2             = p2
        self.turn           = 1       # 1 for P1, -1 for P2
        
        self.pieces = {0 : '-', 
                       1 : '2', -1 : '-2',
                       2 : '3', -2 : '-3',
                       3 : '9', -1 : '-9',
                       4 : '10', -2 : '-10',
                       5 : 'S', -1 : '-S',
                       6 : 'B', -2 : '-B',
                       7 : 'F', -2 : '-F'
                       }

    
    def action_space(board):
        
        # Return pieces that changed in the board
        # Tuples containing (x, y, new_value, x2, y2, new_value)
        return possible_actions
    
    # Request an action from the current player
    def req_action(self, reward):
        if(self.turn==1):
            c_player = self.p1
            c_board  = self.board_p1
        else:
            c_player = self.p2
            c_board  = self.board_p2
            
        actions = action_space(self.c_board)
        action_idx = self.c_player.play(self.c_board, actions, reward)
        
        # Environment has to check if best action is possible
        if action_idx >= len(actions):
            print("Invalid Move")

        return actions[action_idx]
    
    def update(self, best_action):
        self.save_board()
        self.update_board(best_action)                  # Update global board
        self.update_current_board(best_action)          # Update current player board
        self.update_opp_board(best_action)              # Update opponent's board 
        self.end_turn()
    
    def save_board(self):
        if(self.turn):
            self.prev_board_p1 = deepcopy(self.board_p1)
        else:
            self.prev_board_p2 = deepcopy(self.board_p2)
        
    def end_turn(self):
        self.turn *= -1

    def print_board(self):
        print(self.board)


p1 = Agent()
p2 = Agent()
stratego = Environment(p1, p2)

stratego.board[:3 ,:] = p1.setup() 
stratego.board[5:8,:] = p2.setup()
stratego.print_board()
exit()
while game_not_ended:
    
    reward, done = stratego.calc_reward()
    if(done):
        # Update both p1 & p2
        break
    
    best_action = stratego.req_action(reward_p1)
    stratego.update(best_action)
