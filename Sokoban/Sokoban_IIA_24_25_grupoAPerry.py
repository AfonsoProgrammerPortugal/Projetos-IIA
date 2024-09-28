from searchPlus import *

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


class Sokoban(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        pass
   
    def actions(self, state):
        pass
        
    def result(self, state, action):
        pass
        
    def executa(self,state,actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate=state
        for a in actions:
            nstate=p.result(nstate,a)
        return nstate
    
    def display(self, state):
        """Devolve a grelha em modo txt"""
        pass