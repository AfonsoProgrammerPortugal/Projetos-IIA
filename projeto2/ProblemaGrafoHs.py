from searchPlus import *

class ProblemaGrafoHs(Problem) :
    grafo = {'I':{'A':2,'B':6},
             'A':{'C':2,'D':4,'I':2},
             'B':{'D':1,'F':5,'I':6},
             'C':{},
             'D':{'C':2,'F':2},
             'F':{}}

    def __init__(self,initial = 'I', final = 'F') :
        super().__init__(initial,final)
        
    def actions(self,estado) :
        sucessores = self.grafo[estado].keys()  # métodos keys() devolve a lista das chaves do dicionário
        accoes = list(map(lambda x : "ir de {} para {}".format(estado,x),sucessores))
        return accoes

    def result(self, estado, accao) :
        """Assume-se que uma acção é da forma 'ir de X para Y'
        """
        return accao.split()[-1]
    
    def path_cost(self, c, state1, action, state2):
        return c + self.grafo[state1][state2]

    def h1(self,no) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'I':7, 'A':6,'B':2,'C':4,'D':2,'F':0}
        return h[no.state]
    
    def h2(self,no) : 
        h = {'I':10, 'A':4,'B':5,'C':5,'D':2,'F':0}
        return h[no.state]