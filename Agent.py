import numpy as np

def one_hot(lst, size):
    return np.eye(size)[np.array([lst]).reshape(-1)]


def one_hot_to_idx(one_hot_lst):
    print(np.where(one_hot_lst))
    return [ np.where(r==1)[0][0] for r in one_hot_lst[0] ]


class Agent:
    
    def __init__(self):
        pass
    
    def play(self, state, actions, reward):
        actions = self.getActions(state)
        return best_action

    def setup(self, pieces, setup_area):
        setup = np.zeros(setup_area)
        setup[0][0] = pieces[9]
        setup[0][1] = pieces[8]
        setup[0][2] = pieces[3]
        setup[0][3] = pieces[2]
        setup[0][4] = pieces[0]
        
        setup[1][0] = pieces[7]
        setup[1][1] = pieces[6]
        setup[2][2] = pieces[1]
        setup[1][3] = pieces[4]
        setup[1][4] = pieces[5]
        return setup


