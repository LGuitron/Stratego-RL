import numpy as np
from copy import deepcopy
from Agent import Agent
from TinyAgent import TinyAgent

class Environment:
    
    def __init__(self, p1, p2):
        
        self.board_size = (4,4)
        #self.board_size  = (8,8)
        #self.setup_area  = (3, self.board_size[1])
        self.setup_area  = (2, self.board_size[1])
        self.unknown_key = -102
        self.impassable  = 103

        # Piece information                (Movable, Print Char, ...)
        self.cell_properties = {    0   : {"movable": False, "print":'  -  '},
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

        self.board          = np.zeros(self.board_size, dtype=np.int32) 

        # Values for P1 and P2 in arrays
        self.rewards               = np.zeros(2)
        self.players               = [p1, p2]
        self.player_boards         = [np.zeros(self.board_size, dtype=np.int32) , np.zeros(self.board_size, dtype=np.int32)]
        self.prev_player_boards    = [None, None]
        
        self.turn            = 0                     # 0 for P1, 1 for P2

        self.impassable_coords = [(3,2),(4,2),(3,5),(4,5)]
        self.pieces            = [1,2,2,3,3,9,10,99,99,101]

        # Initialize graveyard arrays for both players
        self.unique_pieces = set(self.pieces)
        self.graveyard         = [np.zeros(len(set(self.pieces))),np.zeros(len(set(self.pieces)))]
        
        #Validate p1 & p2 setup
        self.init_boards()
    
    def validate_setup(self):
        pass

    def init_boards(self):   
         
         
        self.board[:self.setup_area[0]] = p1.setup(self.pieces, self.setup_area)
        self.board[-self.setup_area[0]:] = -p2.setup(self.pieces, self.setup_area)
        self.validate_setup()
         
         
        # Player Boards
        # P1 perspective
        for i in range(self.setup_area[0]):
            for j in range(self.board_size[1]):
                if(self.board[i][j]!=0):
                    self.player_boards[0][i][j] = self.board[i][j]
                    self.player_boards[1][i][j] = self.unknown_key
                    
        # P2 perspective
        for i in range(self.board_size[0] - self.setup_area[0],self.board_size[0]):
            for j in range(self.board_size[1]):
                if(self.board[i][j]!=0):
                    self.player_boards[0][i][j] = self.unknown_key
                    self.player_boards[1][i][j] = -self.board[i][j]
    
        # Place impassables
        '''
        for coord in self.impassable_coords:
            x , y = coord
            self.board[x][y]    = self.impassable
            self.player_boards[0][x][y] = self.impassable
            self.player_boards[1][x][y] = self.impassable
        '''

    # Request an action from the current player
    def req_action(self, actions, reward):
        selected_action = self.players[self.turn].play([self.player_boards[self.turn] , self.graveyard] , actions, reward)
        actions
        if selected_action not in actions:
            print("Invalid Move")
        
        return selected_action

    # Get all possible states for current position
    def action_space(self):
        
        movements = []

        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                movements += self.piece_movements(i,j)
        return movements
        
    # Find the possible movements for a given piece
    # Return List of Tuples containing ((x0,y0), (x1,y1), new_val on (x1,y1))
    def piece_movements(self, i, j):

        c_cell = self.player_boards[self.turn][i][j]
        source = (i,j)
        movements = []

        dirs = [-1, 0, 1, 0]
        
        if((c_cell <= 0) or not self.cell_properties[c_cell]['movable']):
            return movements

        # Long move for the scout
        elif "long_move" in self.cell_properties[c_cell]:
            
            for k in range(4):
                
                #for step_size in range(self.board_size[k%2])
                step_size = 1
                while True:
                    x, y = i + step_size*dirs[k], j + step_size*dirs[(k+1) % 4]
                    
                    # Check boundaries, and target cell
                    if(x >= self.board_size[0] or y >= self.board_size[1] or x < 0 or y < 0 or self.player_boards[self.turn][x][y] > 0 or self.player_boards[self.turn][x][y] == self.impassable):
                        break
                    
                    movements.append((source, (x,y)))
                    
                    # Attacking opponent piece
                    if self.player_boards[self.turn][x][y] < 0:
                        break
                    
                    step_size += 1

        # Regular move for the rest of the pieces
        else:
            for k in range(4):
                x, y = i + dirs[k], j + dirs[(k+1) % 4]
                
                # Check boundaries, and target cell
                if(x >= self.board_size[0] or y >= self.board_size[1] or x < 0 or y < 0 or self.player_boards[self.turn][x][y] > 0 or self.player_boards[self.turn][x][y] == self.impassable):
                    continue 
                movements.append((source, (x,y)))
        

        return movements

    # Returns reward based on current board
    # and return if game is over or not
    def calc_reward(self, action_size):
        
        # Check if current player lost
        # Lost Flag or No amoves available
        if (101 not in self.player_boards[self.turn] or action_size==0):
            if(101 not in self.player_boards[self.turn]):
                pass
                #print("LOST FLAG")
            else:
                pass
                #print("NO MORE MOVES")
                
            if(self.turn==1):
                pass
                #print("P2 won")
            else:
                pass
                #print("P1 won")
            return -1, True
        
        
        
        #Calculate the reward of the current board
        reward = -0.001
        
        
        return reward, False

    
    def update(self, selected_action):
        self.save_board()
        self.update_boards(selected_action)                  # Update global board
        self.next_turn()
    

    def update_boards(self, selected_action):
        source = selected_action[0]
        dest = selected_action[1]
        piece_player = self.board[source]
        piece_opp = self.board[dest]
        
        self.board[source]    = 0
        self.player_boards[0][source] = 0
        self.player_boards[1][source] = 0



        # Current player wins (against opponent or enemy flag or miner diffuses bomb)
        if(abs(piece_player) > abs(piece_opp)                     # General combat, or place occupation
           or abs(piece_opp)==101                                 # Against flag
           or(abs(piece_player)==3 and abs(piece_opp)==99)        # Miner diffuses bomb 
           or(abs(piece_player)==1 and abs(piece_opp)==10)):      # Spy vs Marshall
            
            
            self.board[dest]     =  piece_player
            self.player_boards[self.turn][dest]   =  abs(piece_player)
            
            # Moved to empty space
            if(piece_opp==0):
                self.player_boards[1-self.turn][dest] =  self.unknown_key

            # Defeated opponent piece
            # Reveal attacking piece to opponent, and update graveyard
            else:
                self.player_boards[1-self.turn][dest] = -abs(piece_player)
                self.graveyard[1-self.turn][self.cell_properties[abs(piece_opp)]["grave_index"]] += 1
                
        # Opponent wins
        # Reveal attacked player, and update graveyard
        elif(abs(piece_player) < abs(piece_opp)):
            self.board[dest]                      =  piece_opp
            self.player_boards[self.turn][dest]   =  -abs(piece_opp)
            self.graveyard[self.turn][self.cell_properties[abs(piece_player)]["grave_index"]] += 1
            
        # Pieces have same value
        # Both of them die, update graveyards
        else:
            self.board[dest]                        =  0
            self.player_boards[self.turn][dest]     =  0
            self.player_boards[1-self.turn][dest]   =  0
            self.graveyard[self.turn][self.cell_properties[abs(piece_player)]["grave_index"]] += 1
            self.graveyard[1-self.turn][self.cell_properties[abs(piece_opp)]["grave_index"]] += 1
        
        
    def save_board(self):
        self.prev_player_boards[self.turn] = deepcopy(self.player_boards[self.turn])
        self.prev_player_boards[1-self.turn] = deepcopy(self.player_boards[1-self.turn])
        
    def next_turn(self):
        self.turn = 1 - self.turn

    def print_board(self, board):
        
        print()
        print(self.graveyard[0])
        
        for i in range(board.shape[0]):
            row = "["
            for j in range(board.shape[1]):
                #if
                if(board[i,j] >= 0 or board[i,j]==self.unknown_key):
                    row += self.cell_properties[board[i,j]]["print"]
                else:
                    row += " -" + self.cell_properties[-board[i,j]]["print"][2:]
            print(row + "]")
        print(self.graveyard[1])
        print()
#p1 = Agent()
#p2 = Agent(is_p1 = False)
p1 = TinyAgent()
p2 = TinyAgent(is_p1 = False)
game_stats = np.zeros(2)
num_games = 1
for i in range(num_games):

    stratego = Environment(p1, p2)    
    
    while True:
        actions = stratego.action_space()
        reward, done = stratego.calc_reward(len(actions))
        if(done):
            if(stratego.turn==1):
                game_stats[0] += 1
            else:
                game_stats[1] += 1

            # Send winning and losing rewards to the players
            stratego.players[stratego.turn].receive_last_reward(reward)
            stratego.players[1-stratego.turn].receive_last_reward(-reward)
            #stratego.print_board(stratego.board)
            
            break
        
        selected_action = stratego.req_action(actions, reward)
        stratego.update(selected_action)

print(game_stats/num_games)
