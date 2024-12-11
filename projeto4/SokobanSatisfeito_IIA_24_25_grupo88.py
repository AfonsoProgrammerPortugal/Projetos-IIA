from sokoban_aval4 import *

linha1= "    ####\n"
linha2= "  ##...#\n"
linha3= "###....#\n"
linha4= "#o..$#@#\n"
linha5= "#oo$.$.#\n"
linha6= "###o.$.#\n"
linha7= "  ###..#\n"
linha8= "    ####\n"
mundoS=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8

alcancaveis={(1, 4): [], (1, 5): [], (1, 6): [], (2, 3): [], (2, 4): [(3, 1), (4, 1), (4, 2), (5, 3)], (2, 5): [(3, 1), (4, 1), (4, 2), (5, 3)], (2, 6): [], (3, 1): [(3, 1)], (3, 2): [(3, 1), (4, 1), (4, 2), (5, 3)], (3, 3): [(3, 1), (4, 1), (4, 2), (5, 3)], (3, 4): [(3, 1), (4, 1), (4, 2), (5, 3)], (3, 6): [], (4, 1): [(4, 1)], (4, 2): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 3): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 4): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 5): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 6): [], (5, 3): [(5, 3)], (5, 4): [(3, 1), (4, 1), (4, 2), (5, 3)], (5, 5): [(3, 1), (4, 1), (4, 2), (5, 3)], (5, 6): [], (6, 5): [], (6, 6): []}

################################################################################
# Funções para csp_possivel_solucao
################################################################################

def possivel_solucao(caixas,goals_alcancaveis):
    csp_sokoban1 = csp_possivel_solucao(caixas,goals_alcancaveis) # <--- a vossa função csp_possivel_solucao 
    r = backtracking_search(csp_sokoban1, inference = forward_checking)
    return r

def csp_possivel_solucao(caixas,goals_alcancaveis):
    # TODO: Implemente esta função
    return None

################################################################################
# Testes
################################################################################
# Resultado esperado:
#    Variáveis: [(3, 4), (4, 3), (4, 5), (5, 5)]
#    Domínios: {(3, 4): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 3): [(3, 1), (4, 1), (4, 2), (5, 3)], (4, 5): [(3, 1), (4, 1), (4, 2), (5, 3)], (5, 5): [(3, 1), (4, 1), (4, 2), (5, 3)]}
#    Vizinhos: {(3, 4): [(4, 3), (4, 5), (5, 5)], (4, 3): [(3, 4), (4, 5), (5, 5)], (4, 5): [(3, 4), (4, 3), (5, 5)], (5, 5): [(3, 4), (4, 3), (4, 5)]}
#    Restrição obedecida? False
#    Restrição obedecida? True
s = Sokoban(situacaoInicial=mundoS)
caixas = s.initial['caixas']
csp_sokoban1 = csp_possivel_solucao(caixas,alcancaveis)

print('Variáveis:',sorted(csp_sokoban1.variables))
print('Domínios:',dict(sorted(csp_sokoban1.domains.items())))
sorted_neighbors = {key: sorted(values) for key, values in sorted(csp_sokoban1.neighbors.items())}
print('Vizinhos:',dict(sorted(sorted_neighbors.items())))
print('Restrição obedecida?',csp_sokoban1.constraints((3,4),(3,1),(4,3),(3,1)))
print('Restrição obedecida?',csp_sokoban1.constraints((3,4),(3,1),(4,3),(4,1)))
################################################################################
# Resultado esperado: {(3, 4): (4, 2), (4, 3): (5, 3), (4, 5): (3, 1), (5, 5): (4, 1)}
'''s = Sokoban(situacaoInicial=mundoS)
caixas = s.initial['caixas']
result = possivel_solucao(caixas,alcancaveis) # <--- usa a vossa função csp_possivel_solucao
if result != None:
    result = dict(sorted(result.items()))
print(result)'''
################################################################################
# Resultado esperado: None
'''s = Sokoban(situacaoInicial=mundoS)
caixas = s.initial['caixas']
result = possivel_solucao(caixas,alcancaveis) # <--- usa a vossa função csp_possivel_solucao
if result != None:
    result = dict(sorted(result.items()))
print(result)'''