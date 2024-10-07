from searchPlus import *
import copy

linha1= "  ##### \n"
linha2= "###...# \n"
linha3= "#o@$..# \n"
linha4= "###.$o# \n"
linha5= "#o##..# \n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9

#  #   (cardinal)   Parede
#  o   (ó)          Objectivo vazio
#  @   (arroba)     Sokoban no chão
#  +   (soma)       Sokoban num objectivo
#  $   (dólar)      Caixa no chão
#  *   (asterisco)  Caixa no objectivo

######################## metodos auxiliares #############################

# metodo para obter as duas posicoes seguintes na direcao dada
def get_target_and_next_coords(row, col, direction):
    r, c = row, col
    if direction == "N":   return r-1, c, r-2, c
    elif direction == "W": return r, c-1, r, c-2
    elif direction == "E": return r, c+1, r, c+2
    else:                  return r+1, c, r+2, c

# metodo que verifica se uma dada posicao
# configura um canto invalido para um certa matriz
def is_invalid_corner(row, col, world):
    return (world[row - 1][col] == "#" and world[row][col + 1] == "#") or \
            (world[row][col + 1] == "#" and world[row + 1][col] == "#") or \
            (world[row + 1][col] == "#" and world[row][col - 1] == "#") or \
            (world[row][col - 1] == "#" and world[row - 1][col] == "#")

# metodo para processar uma string que representa um mundo
# do sokoban, retornando o estado atual do jogo, a matriz
# layout do mundo, o conjunto dos cantos e dos objetivos
def process_world(initial_world):
    world = [list(row) for row in initial_world.split("\n")]
    state = {"sokoban": tuple(), "boxes": set()}
    corners = set()
    objectives = set()

    for row in range(len(world)):
        for col in range(len(world[row])):
            char = world[row][col]

            if char in "@+":
                state["sokoban"] = (row, col)
                if is_invalid_corner(row, col, world):
                    corners.add((row, col))
                if char == "+":
                    world[row][col] = "o"
                    objectives.add((row, col))
                else:
                    world[row][col] = "."

            elif char in "$*":
                state["boxes"].add((row, col))
                if char == "*":
                    world[row][col] = "o"
                    objectives.add((row, col))
                else:
                    world[row][col] = "."

            elif char == "." and is_invalid_corner(row, col, world):
                corners.add((row, col))

            elif char == "o":
                objectives.add((row, col))

    return state, world, corners, objectives

# metodo que diz se há uma caixa em uma dada posicao para um dado estado
def is_box(row, col, state):
    return (row, col) in state["boxes"]

############################ SokobanProblem ###############################

class Sokoban(Problem):
    def __init__(self, situacaoInicial = mundoStandard):
        self.initial, self.layout, self.corners, self.objectives = process_world(situacaoInicial)
        super().__init__(self.initial)

    def actions(self, state):
        return [direction for direction in "NWES" if self.can_move(direction, state)]

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        direction = action
        r, c = state["sokoban"]
        r_target, c_target, r_next, c_next = get_target_and_next_coords(r, c, direction)

        # nova posicao do Sokoban
        new_state["sokoban"] = (r_target, c_target)

        # mover caixa se existir alguma na posicao
        if is_box(r_target, c_target, state):
            new_state["boxes"].remove((r_target, c_target))
            new_state["boxes"].add((r_next, c_next))

        return new_state

    # Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado
    def executa(self, state, actions):
        new_state = state

        for action in actions:
            new_state = self.result(new_state, action)

        return new_state

    def goal_test(self, state):
        return state["boxes"] == self.objectives

    def display(self, state):
        result = copy.deepcopy(self.layout)
        sokoban_r, sokoban_c = state["sokoban"]

        if (sokoban_r, sokoban_c) in self.objectives:
            result[sokoban_r][sokoban_c] = "+"
        else:
            result[sokoban_r][sokoban_c] = "@"

        for box_r, box_c in state["boxes"]:
            if (box_r, box_c) in self.objectives:
                result[box_r][box_c] = "*"
            else:
                result[box_r][box_c] = "$"

        result = ["".join(row) for row in result]
        result_str = "\n".join(result)

        return result_str

    # metodo que verifica se uma dada posicao esta vazia,
    # considerando para isso o layout do mundo e o estado dado
    def is_empty(self, row, col, state):
        return (self.layout[row][col] in ".o" and
                state["sokoban"] != (row, col) and
                not is_box(row, col, state))

    # metodo que verifica se um dado movimento eh
    # valido para o mundo e o estado em causa
    def can_move(self, direction, state):
        r, c = state["sokoban"]
        r_target, c_target, r_next, c_next = get_target_and_next_coords(r, c, direction)

        return self.is_empty(r_target, c_target, state) or \
              (is_box(r_target, c_target, state) and self.is_empty(r_next, c_next, state) and
              (r_next, c_next) not in self.corners)
