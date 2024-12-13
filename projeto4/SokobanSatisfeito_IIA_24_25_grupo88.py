from csp_v3 import *
from searchPlus import *
from sokoban_aval4 import *
from search import *
import copy

def csp_possivel_solucao(caixas, goals_alcancaveis):
    variaveis = list(copy.deepcopy(caixas))

    dominios = {}
    for celula, goals in goals_alcancaveis.items():
        if celula in variaveis:
            dominios[celula] = goals

    vizinhos = {}
    for caixa in variaveis:
        meu_dominio = dominios[caixa]
        if meu_dominio:
            for outra_caixa in variaveis:
                if outra_caixa != caixa and bool(set(meu_dominio) & set(dominios[outra_caixa])):
                    if caixa in vizinhos:
                        vizinhos[caixa].append(outra_caixa)
                    else:
                        vizinhos[caixa] = [outra_caixa]

    def restricoes(X, a, Y, b):
        if Y in vizinhos[X]:
            return a != b
        return True

    return CSP(variaveis, dominios, vizinhos, restricoes)

# ------------------------------------------------------------------------------------------------------------------------------

def vizinhos_mesma_linha(celula1, celula2, navegaveis):
    l1, c1 = celula1
    l2, c2 = celula2

    return l1 == l2 and \
           ((c1 == c2 - 1 and ((l1, c1 - 1) in navegaveis or (l1, c2 + 1) in navegaveis)) or
            (c1 == c2 + 1 and ((l1, c1 + 1) in navegaveis or (l1, c2 - 1) in navegaveis)))

def vizinhos_mesma_coluna(celula1, celula2, navegaveis):
    l1, c1 = celula1
    l2, c2 = celula2

    return c1 == c2 and \
           ((l1 == l2 - 1 and ((l1 - 1, c1) in navegaveis or (l2 + 1, c1) in navegaveis)) or
            (l1 == l2 + 1 and ((l1 + 1, c1) in navegaveis or (l2 - 1, c1) in navegaveis)))

def sao_vizinhos(celula1, celula2, navegaveis):
    return vizinhos_mesma_linha(celula1, celula2, navegaveis) or \
           vizinhos_mesma_coluna(celula1, celula2, navegaveis)

def diferentes(x,y):
    """x diferente de y"""
    return x != y

def csp_find_alcancaveis_1goal(s, goal):
    variaveis = list(copy.deepcopy(s.navegaveis))

    dominios = {}
    for celula in variaveis:
        if celula == goal:
            dominios[celula] = [1]
        elif s.its_a_trap(celula):
            dominios[celula] = [0]
        else: 
            dominios[celula] = [0, 1]

    vizinhos = {}
    for celula in variaveis:
        for outra_celula in variaveis:
            if outra_celula != celula and sao_vizinhos(celula, outra_celula, variaveis):
                if celula in vizinhos:
                    vizinhos[celula].append(outra_celula)
                else:
                    vizinhos[celula] = [outra_celula]
    
    def restricoes(X, a, Y, b):
        if a == 1 and not s.its_a_trap(Y) and b == 0:
            return False
        if b == 1 and not s.its_a_trap(X) and a == 0:
            return False
        return True

    return CSP(variaveis, dominios, vizinhos, restricoes)  

#----------------------------------------------------------------------------------------------------------

def possivel_solucao(caixas,goals_alcancaveis):
    csp_sokoban1 = csp_possivel_solucao(caixas,goals_alcancaveis) # <--- a vossa função csp_possivel_solucao 
    r = backtracking_search(csp_sokoban1, inference = forward_checking)
    return r
    
def find_alcancaveis_1goal(s,goal):
    csp_sokoban2 = csp_find_alcancaveis_1goal(s,goal) # <--- a vossa função csp_find_alcancaveis_1goal 
    r = backtracking_search(csp_sokoban2, order_domain_values = number_ascending_order, inference = forward_checking)    
    return {} if r == None else r  
