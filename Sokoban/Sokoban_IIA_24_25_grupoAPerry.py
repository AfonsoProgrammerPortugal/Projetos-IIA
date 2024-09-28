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
        self.world = world

    def completed(self):
        has_completed = True

        for elem in self.world:
            if elem == '$':
                has_completed = False
                break

        return has_completed

    def __eq__(self, other):
        return self.world == other.world

############################ SokobanProblem ###############################

class Sokoban(Problem):
    def __init__(self, initial_world = standard_world):
        self.initial = SokobanState(initial_world)
        super().__init__(self.initial)

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

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