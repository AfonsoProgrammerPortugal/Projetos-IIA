from searchPlus import *

line1 = "  ##### \n"
line2 = "###...# \n"
line3 = "#.o$@.# \n"
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

def get_potential_walls_coords(row, col, direction):
    r, c = row, col
    if direction == "N":   return r-1, c, r, c+1, r, c-1
    elif direction == "W": return r, c-1, r-1, c, r+1, c
    elif direction == "E": return r, c+1, r-1, c, r+1, c
    else:                  return r+1, c, r, c+1, r, c-1

def get_target_and_next_coords(row, col, direction):
    r, c = row, col
    if direction == "N":   return r-1, c, r-2, c
    elif direction == "W": return r, c-1, r, c-2
    elif direction == "E": return r, c+1, r, c+2
    else:                  return r+1, c, r+2, c

class SokobanState:

    def __init__(self, world):
        self.world_str = world
        self.world_grid = self.world_str.rstrip("\n").split("\n")
        self.r, self.c, self.invalid_corners = self.get_sokoban_pos_and_invalid_corners()

    def get_sokoban_pos_and_invalid_corners(self):
        grid = self.world_grid

        sokoban_found = False
        sokoban_row, sokoban_col = 0, 0
        corners = []

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if not sokoban_found and grid[row][col] in "@+":
                    sokoban_found = True
                    sokoban_row, sokoban_col = row, col
                elif grid[row][col] == "." and self.is_invalid_corner(row, col):
                    corners.append((row, col))

        return sokoban_row, sokoban_col, corners

    def is_invalid_corner(self, row, col):
        grid = self.world_grid
        counter = 0

        if grid[row - 1][col] == "#" and grid[row][col + 1] == "#": counter += 1
        if grid[row][col + 1] == "#" and grid[row + 1][col] == "#": counter += 1
        if grid[row + 1][col] == "#" and grid[row][col - 1] == "#": counter += 1
        if grid[row][col - 1] == "#" and grid[row - 1][col] == "#": counter += 1

        return counter >= 2

    def is_empty(self, row, col):
        return self.world_grid[row][col] in ".o"

    def is_box(self, row, col):
        return self.world_grid[row][col] in "*$"

    def can_move(self, direction):
        r, c = self.r, self.c
        r_target, c_target, r_next, c_next = get_target_and_next_coords(r, c, direction)

        return self.is_empty(r_target, c_target) or \
              (self.is_box(r_target, c_target) and self.is_empty(r_next, c_next) and
              (r_next, c_next) not in self.invalid_corners)

    def get_valid_actions(self):
        return [direction for direction in "NWES" if self.can_move(direction)]

    def get_result(self, action):
        new = [list(row) for row in self.world_grid]
        direction = action
        r, c = self.r, self.c
        r_target, c_target, r_next, c_next = get_target_and_next_coords(r, c, direction)
        sokoban_pos_char = self.world_grid[r][c]
        target_pos_char = self.world_grid[r_target][c_target]
        next_pos_char = self.world_grid[r_next][c_next]

        # posiCAo inicial do Sokoban
        if sokoban_pos_char == "+":
            new[r][c] = "o"
        elif sokoban_pos_char == "@":
            new[r][c] = "."

        # posiCAo target vazio
        if target_pos_char in ".o":
            if target_pos_char == ".":
                new[r_target][c_target] = "@"
            elif target_pos_char == "o":
                new[r_target][c_target] = "+"

        # posiCAo target caixa
        elif target_pos_char in "$*":
            if next_pos_char == ".":
                new[r_next][c_next] = "$"
            elif next_pos_char == "o":
                new[r_next][c_next] = "*"
            if target_pos_char in "$":
                new[r_target][c_target] = "@"
            elif target_pos_char == "*":
                new[r_target][c_target] = "+"

        new = ["".join(row) for row in new]
        new_world_str = "\n".join(new)

        return SokobanState(new_world_str)

    def completed(self):
        for elem in self.world_str:
            if elem == '$':
                return False

        return True

    def __eq__(self, other):
        return self.world_str == other.world_str

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
        print(state.world_str)

s = Sokoban()
#print(s.goal_test(SokobanState(standard_world)))
print(s.actions(s.initial))
s1 = s.result(s.initial, "W")
s.display(s1)