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

    def locateSokoban(self, Grid):
        for r in range(len(Grid)):
            for c in range(len(Grid[r])):
                if Grid[r][c] == "@" or Grid[r][c] == "+":
                    return (r,c)

    def __init__(self, world):
        self.world = world
        self.worldGrid = self.world.split("\n")
        self.sokobanPosition = self.locateSokoban(self.worldGrid)
        self.r, self.c = self.sokobanPosition[0], self.sokobanPosition[1]

    def canMoveTo(self, direction):
        result = True
        r, c = self.r, self.c

        #Falta a condiCAo dos cantos
        
        if direction == "N":
            if self.worldGrid[r-1][c] == "#" or \
                (self.worldGrid[r-1][c] == "$" and self.worldGrid[r-2][c] not in ".o"):
                result = False
        if direction == "W":
            if self.worldGrid[r][c-1] == "#" or \
                (self.worldGrid[r][c-1] == "$" and self.worldGrid[r][c-2] not in ".o"):
                result = False
        if direction == "E":
            if self.worldGrid[r][c+1] == "#" or \
                (self.worldGrid[r][c+1] == "$" and self.worldGrid[r][c+2] not in ".o"):
                result = False
        if direction == "S":
            if self.worldGrid[r+1][c] == "#" or \
                (self.worldGrid[r+1][c] == "$" and self.worldGrid[r+2][c] not in ".o"):
                result = False

        return result

    def getActions(self):
        actions = []

        #Caso esteja uma parede ("#")
        if self.canMoveTo("N"):
            actions.append("N")

        if self.canMoveTo("W"):
            actions.append("W")

        if self.canMoveTo("E"):
            actions.append("E")

        if self.canMoveTo("S"):
            actions.append("S")

        return actions
    
    def getResult(self, action):
        pass

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
        return state.getActions()

    def result(self, state, action):
        return state.getResult(action)

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