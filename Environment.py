import numpy as np
from copy import deepcopy
from Agent import Agent

class Environment:
    
    def __init__(self, p1, p2):
        
        self.board_size  = (8,8)
        self.setup_area  = (3, self.board_size[1])
        self.unknown_key = -102
        self.impassable  = 103

        # Piece information                (Movable, Print Char, ...)
        self.cell_properties = {    0   : {"movable": False, "print":'  -  '},
                                    1   : {"movable": True,  "print":'  S  '},
                                    2   : {"movable": True,  "print":'  2  ', "long_move" : None},
                                    3   : {"movable": True,  "print":'  3  '},  
                                    9   : {"movable": True,  "print":'  9  '},  
                                    10  : {"movable": True,  "print":'  10 '}, 
                                    99  : {"movable": False, "print":'  B  '},
                                    101 : {"movable": False, "print":'  F  '},
                                    self.unknown_key : {"movable": False, "print":'  U  '},
                                    self.impassable  : {"movable": False, "print":'  X  '}
                                }

        self.board          = np.zeros(self.board_size) 
        self.board_p1       = np.zeros(self.board_size) 
        self.board_p2       = np.zeros(self.board_size)
        self.prev_board_p1  = None
        self.prev_board_p2  = None
        
        self.c_player = None          # Current player
        self.c_board  = None          # Board from the current player's perspective

        self.p1             = p1
        self.p2             = p2
        self.turn           = 1       # 1 for P1, -1 for P2

        self.impassable_coords = [(3,2),(4,2),(3,5),(4,5)]
        self.pieces            = [1,2,2,3,3,9,10,99,99,101]
        
        

        
        #Validate p1 & p2 setup
        
        #self.init_player_boards()
        self.init_boards()
        self.start_turn()
        
        self.print_board(self.board)
        self.print_board(self.board_p1)
        self.print_board(self.board_p2)
    
    def validate_setup(self):
        pass

        
    #def init_player_boards(self):
    def init_boards(self):   
         
         
        self.board[:self.setup_area[0]] = p1.setup(self.pieces, self.setup_area)
        self.board[-self.setup_area[0]:] = -p2.setup(self.pieces, self.setup_area)
        self.validate_setup()
         
         
        # Player Boards
        # P1 perspective
        for i in range(self.setup_area[0]):
            for j in range(self.board_size[1]):
                if(self.board[i][j]!=0):
                    self.board_p1[i][j] = self.board[i][j]
                    self.board_p2[i][j] = self.unknown_key
                    
        # P2 perspective
        for i in range(self.board_size[0] - self.setup_area[0],self.board_size[0]):
            for j in range(self.board_size[1]):
                if(self.board[i][j]!=0):
                    self.board_p1[i][j] = self.unknown_key
                    self.board_p2[i][j] = -self.board[i][j]
    
        # Place impassables
        for coord in self.impassable_coords:
            x , y = coord
            self.board[x][y]    = self.impassable
            self.board_p1[x][y] = self.impassable
            self.board_p2[x][y] = self.impassable
    
    # Set member variables required for this turn
    def start_turn(self):
    
        if(self.turn==1):
            self.c_player = self.p1
            self.c_board  = self.board_p1
        else:
            self.c_player = self.p2
            self.c_board  = self.board_p2

    # Request an action from the current player
    def req_action(self, reward):
        
        if(self.turn==1):
            self.c_player = self.p1
            self.c_board  = self.board_p1
        else:
            self.c_player = self.p2
            self.c_board  = self.board_p2
            
        actions = self.action_space()
        action_idx = self.c_player.play(self.c_board, actions, reward)
        
        # Environment has to check if best action is possible
        if action_idx >= len(actions):
            print("Invalid Move")

        return actions[action_idx]

    
        
    

    def action_space(self):
        
        movements = []

        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                c_cell = self.c_board[i][j]
                if(self.cell_properties[c_cell]['movable']):
                    movements += self.piece_movements(i,j)

        return movements
        
    # Find the possible movements for a given piece
    # Return List of Tuples containing ((x0,y0), (x1,y1), new_val on (x1,y1))
    def piece_movements(self, i, j):
        
        c_cell = self.board[i][j]
        source = (i,j)
        movements = []

        dirs = [-1, 0, 1, 0]


        if "long_move" in self.cell_properties[c_cell]:
            
            for k in range(4):
                
                #for step_size in range(self.board_size[k%2])
                step_size = 1
                while True:
                    x, y = i + step_size*dirs[k], j + step_size*dirs[(k+1) % 4]
                    
                    # Check boundaries, and target cell
                    if(x >= self.board_size[0] or y >= self.board_size[1] or x < 0 or y < 0 or self.c_board[x][y] > 0):
                        break
                    movements.append((source, (x,y), c_cell))
                    step_size += 1

        else:
            for k in range(4):
                x, y = i + dirs[k], j + dirs[(k+1) % 4]
                
                # Check boundaries, and target cell
                if(x >= self.board_size[0] or y >= self.board_size[1] or x < 0 or y < 0 or self.c_board[x][y] > 0):
                    continue 
                movements.append((source, (x,y), c_cell))
        

        return movements

    # Returns reward based on current board
    # and return if game is over or not
    def calc_reward(self):
        
        # Check if current player lost
        if (101 not in self.c_board):
            return -1000, True
        
        #Calculate the reward of the current board
        reward = 0
        
        
        return reward, False

    
    def update(self, best_action):
        self.start_turn()
        self.save_board()
        self.update_board(best_action)                  # Update global board
        self.update_current_board(best_action)          # Update current player board
        self.update_opp_board(best_action)              # Update opponent's board 
        self.end_turn()
    

    
    
    def save_board(self):
        #if(self.turn):
        self.prev_board_p1 = deepcopy(self.board_p1)
        #else:
        self.prev_board_p2 = deepcopy(self.board_p2)
        
    def end_turn(self):
        self.turn *= -1

    def print_board(self, board):
        print()
        for i in range(board.shape[0]):
            row = "["
            for j in range(board.shape[1]):
                #if
                if(board[i,j] >= 0 or board[i,j]==self.unknown_key):
                    row += self.cell_properties[board[i,j]]["print"]
                else:
                    row += " -" + self.cell_properties[-board[i,j]]["print"][2:]
            print(row + "]")
        print()

p1 = Agent()
p2 = Agent()
stratego = Environment(p1, p2)

#stratego.board[:3 ,:] = p1.setup() 
#stratego.board[5:8,:] = p2.setup()


    


#stratego.print_board()
#exit()
while True:
    
    reward, done = stratego.calc_reward()
    if(done):
        # Update both p1 & p2
        break
    
    best_action = stratego.req_action(reward)
    stratego.update(best_action)
