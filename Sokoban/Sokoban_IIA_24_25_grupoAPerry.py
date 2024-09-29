from searchPlus import *

line1 = "  ##### \n"
line2 = "###...# \n"
line3 = "#o@$..# \n"
line4 = "###.$o# \n"
line5 = "#o##..# \n"
line6 = "#.#...##\n"
line7 = "#$.....#\n"
line8 = "#......#\n"
line9 = "########\n"
standard_world = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9

#  #   (cardinal)   Parede
#  o   (ó)          Objectivo vazio
#  @   (arroba)     Sokoban no chão
#  +   (soma)       Sokoban num objectivo
#  $   (dólar)      Caixa no chão
#  *   (asterisco)  Caixa no objectivo

############################ SokobanState ###############################

class SokobanState:

    def __init__(self, world):
        self.world_str = world
        self.world_grid = self.world_str.split("\n")
        self.r, self.c = self.get_sokoban_pos()

    def get_sokoban_pos(self):
        for row in range(len(self.world_grid)):
            for col in range(len(self.world_grid[row])):
                if self.world_grid[row][col] in "@+":
                    return row, col

    def is_empty(self, row, col):
        return self.world_grid[row][col] in ".o"

    def is_box(self, row, col):
        return self.world_grid[row][col] in "*$"
    
    def is_invalid_corner(self, row, col, direction):
        
        if direction == "N": 
            return self.world_grid[row-1][col] == "#" and \
                   (self.world_grid[row][col+1] == "#" or \
                    self.world_grid[row][col-1] == "#") and \
                    self.world_grid[row][col] != "o"
        
        if direction == "W": 
            return self.world_grid[row][col-1] == "#" and \
                   (self.world_grid[row-1][col] == "#" or \
                    self.world_grid[row+1][col] == "#") and \
                    self.world_grid[row][col] != "o"
        
        if direction == "E": 
            return self.world_grid[row][col+1] == "#" and \
                   (self.world_grid[row-1][col] == "#" or \
                    self.world_grid[row+1][col] == "#") and \
                    self.world_grid[row][col] != "o"
        
        if direction == "S": 
            return self.world_grid[row+1][col] == "#" and \
                   (self.world_grid[row][col+1] == "#" or \
                    self.world_grid[row][col-1] == "#") and \
                    self.world_grid[row][col] != "o"

    def can_move(self, direction):
        r, c = self.r, self.c

        if direction == "N":   r_target, c_target, r_next, c_next = r-1, c, r-2, c
        elif direction == "W": r_target, c_target, r_next, c_next = r, c-1, r, c-2
        elif direction == "E": r_target, c_target, r_next, c_next = r, c+1, r, c+2
        else:                  r_target, c_target, r_next, c_next = r+1, c, r+2, c

        return self.is_empty(r_target, c_target) or \
               self.is_box(r_target, c_target) and self.is_empty(r_next, c_next) and not \
               self.is_invalid_corner(r_next, c_next, direction)

    def get_valid_actions(self):
        return [direction for direction in "NWES" if self.can_move(direction)]
    
    def get_result(self, action):
        r, c = self.r, self.c

        if action == "N":   r_target, c_target, r_next, c_next = r-1, c, r-2, c
        elif action == "W": r_target, c_target, r_next, c_next = r, c-1, r, c-2
        elif action == "E": r_target, c_target, r_next, c_next = r, c+1, r, c+2
        else:               r_target, c_target, r_next, c_next = r+1, c, r+2, c

        return 

    def completed(self):
        has_completed = True

        for elem in self.world_str:
            if elem == '$':
                has_completed = False
                break

        return has_completed

    def __eq__(self, other):
        return self.world_str == other.world

############################ SokobanProblem ###############################

class Sokoban(Problem):
    def __init__(self, initial_world = standard_world):
        self.initial = SokobanState(initial_world)
        super().__init__(self.initial)

    def actions(self, state):
        return state.get_valid_actions()

    def result(self, state, action):
        return state.get_result(action)

    # Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado
    def executa(self, state, actions):
        new_state = state

        for action in actions:
            new_state = self.result(new_state, action)

        return new_state

    def goal_test(self, state):
        return state.completed()

    def display(self, state):
        pass

s = Sokoban()
print(s.goal_test(SokobanState(standard_world)))
print(s.actions(s.initial))