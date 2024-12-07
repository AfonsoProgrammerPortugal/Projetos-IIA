from csp_v3 import *
from searchPlus import *
from itertools import combinations
import copy


def manhattan(p,q):
    (x1,y1) = p
    (x2,y2) = q
    return abs(x1-x2) + abs(y1-y2)


def conv_txt(txt):
    linhas=txt.split('\n')
    linhas=[linha for linha in linhas] 
    dados={'caixas':set(), 'objectivos':set(), 'navegáveis':set(), 'paredes':set()}
    map_puzzle={}
    y=0
    for linha in linhas[:-1]:
        x=0
        for c in linha:
            if c=='$':
                dados['caixas'].add((y,x))
                dados['navegáveis'].add((y,x))
            elif c=='@':
                dados['sokoban']=(y,x)
                dados['navegáveis'].add((y,x))
            elif c=='+':
                dados['sokoban']=(y,x)
                dados['objectivos'].add((y,x))
                dados['navegáveis'].add((y,x))
            elif c=='*':
                dados['caixas'].add((y,x))
                dados['objectivos'].add((y,x))
                dados['navegáveis'].add((y,x))
            elif c=='.':
                dados['navegáveis'].add((y,x))
            elif c=='o':
                dados['navegáveis'].add((y,x))
                dados['objectivos'].add((y,x))
            elif c=='#':
                dados['paredes'].add((y,x))
            x+=1
        map_puzzle[y]=x
        y+=1
    dados["mapa"]=map_puzzle
    return dados


class EstadoSokoban(dict): 
    def __hash__(self):
        #print(self['caixas'])
        ll=list(self['caixas'])
        ll.append(self['sokoban'])
        ll.sort()
        return hash(str(ll))
    
    def __lt__(self,other):
        """Um estado é sempre menor do que qualquer outro, para desempate na fila de prioridades"""
        return True


'''linha1= "  #####\n"
linha2= "###...#\n"
linha3= "#o@$..#\n"
linha4= "###.$o#\n"
linha5= "#o##..#\n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9'''

linha1= "    ####\n"
linha2= "  ##...#\n"
linha3= "###....#\n"
linha4= "#o..$#@#\n"
linha5= "#oo$.$.#\n"
linha6= "###o.$.#\n"
linha7= "  ###..#\n"
linha8= "    ####\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8
'''alcancaveis={(1,4): [], (1,5): [], (1,6): [],
             (2,3): [], (2,4): [(3,1),(4,1),(4,2),(5,3)], (2,5): [(3,1),(4,1),(4,2),(5,3)], (2,6): [],
             (3,1): [(3,1)], (3,2): [(3,1),(4,1),(4,2),(5,3)], (3,3): [(3,1),(4,1),(4,2),(5,3)], (3,4): [(3,1),(4,1),(4,2),(5,3)], (3,6): [],
             (4,1): [(4,1)], (4,2): [(3,1),(4,1),(4,2),(5,3)], (4,3): [(3,1),(4,1),(4,2),(5,3)], (4,4): [(3,1),(4,1),(4,2),(5,3)], (4,5): [(3,1),(4,1),(4,2),(5,3)], (4,6): [],
             (5,3): [(5,3)], (5,4): [(3,1),(4,1),(4,2),(5,3)], (5,5): [(3,1),(4,1),(4,2),(5,3)], (5,6): [],
             (6,5): [], (6,6): []}'''


class Sokoban(Problem):
    """O """
    
    dict_actions = {'N': (-1,0), 'W': (0,-1), 'E': (0,1), 'S': (1,0)}

    def __init__(self, initial=None,goal=None,situacaoInicial=mundoStandard,plug_in_function=None):
        """A partir do puzzle em txt geramos um dicionários de onde extráimos:
        * o estado, as posições objectivo, as casas navegáveis, o mapa e as paredes.
        No estado ficamos com a célula (linha,coluna) com a posição do Sokoban e 
        o conjunto das posições das caixas."""
        dados=conv_txt(situacaoInicial)
        self.initial=EstadoSokoban()
        self.initial['sokoban']=dados['sokoban']
        self.initial['caixas']=dados['caixas']
        self.goal=dados['objectivos']
        self.navegaveis=dados['navegáveis']
        self.mapa=dados['mapa']
        self.paredes=dados['paredes']
        self.proibidas=self.calc_traps()
        self.alcancaveis={}#self.csp_find_alcancaveis()
        self.csp_possivel_solucao=plug_in_function
    
    def possible(self,sokoban,caixas,deltas):
        l,c=sokoban
        dl,dc=deltas
        l1,c1=l+dl,c+dc
        if not (l1,c1) in caixas:
            return (l1,c1) in self.navegaveis
        else:
            l2,c2=l1+dl,c1+dc
            return (l2,c2) in self.navegaveis and (l2,c2) not in self.proibidas and (l2,c2) not in caixas
        
    def its_a_trap(self,cel):
        viz=[]
        num_viz=0
        l,c=cel
        deltas=[self.dict_actions[a] for a in self.dict_actions]
        for (dl,dc) in deltas:
            if (l+dl,c+dc) in self.navegaveis:
                num_viz+=1
                viz.append((l+dl,c+dc))
            if num_viz > 2:
                return False
        if num_viz == 1:
            return True
        l1,c1=viz[0]
        l2,c2=viz[1]
        return l1!=l2 and c1!=c2
        
    def calc_traps(self):
        the_traps=set()
        for n in self.navegaveis:
            if not n in self.goal and self.its_a_trap(n):
                the_traps.add(n)
        return the_traps
        
    def actions(self, state):
        sokoban=state['sokoban']
        caixas=state['caixas']
        if self.csp_possivel_solucao(caixas,self.alcancaveis) == None:
            return []
        else:
            return [action for action in self.dict_actions if self.possible(sokoban,caixas,self.dict_actions[action])]
    
    def result(self, state, action):
        clone=copy.deepcopy(state)
        l,c=clone['sokoban']
        dl,dc=self.dict_actions[action]
        l1,c1=l+dl,c+dc
        clone['sokoban']=(l1,c1)
        if (l1,c1) in clone['caixas']:
            l2,c2=l1+dl,c1+dc
            clone['caixas'].remove((l1,c1))
            clone['caixas'].add((l2,c2))
        return clone

    def goal_test(self,state):
        for caixa in state['caixas']:
            if caixa not in self.goal:
                return False
        return True

    def executa(self,state,actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate=state
        for a in actions:
            nstate=self.result(nstate,a)
        return nstate

    def simbolo(self,estado,cel):
        (l,c)=cel
        if estado['sokoban']==(l,c):
            if (l,c) in self.goal:
                return '+'
            return "@"
        elif (l,c) in estado['caixas']:
            if (l,c) in self.goal:
                return '*'
            return '$'
        elif (l,c) in self.goal:
            return 'o'
        elif (l,c) in self.navegaveis:
            return '.'
        elif (l,c) in self.paredes:
            return '#'
        return ' '
        
    def display(self, state):
        """Devolve a grelha em modo txt"""
        puzzle=''
        for l in self.mapa:
            for c in range(self.mapa[l]):
                puzzle+=self.simbolo(state,(l,c))
            puzzle +='\n'
        return puzzle

    def h_util(self, node):
        """Para cada objetivo (lugar de armazenamento), calcula a distância de Manhattan à caixa mais próxima
        que ainda não foi alocada, ignorando a existência de paredes e/ou obstáculos, e aloca essa caixa ao objetivo.
        O valor da heurística é a soma todas estas distâncias + a distância entre o sokoban e a caixa mais longínqua
        que ainda não está arrumada. Se estamos num estado final, devolve 0."""
        clone=copy.deepcopy(node.state)
        ## Satisfaz objectivo?
        if self.goal_test(clone):
            return 0
        soma_distancias = 0
        caixas_disponiveis = clone['caixas'].copy()
        for obj in self.goal:
            if caixas_disponiveis:  # pode haver menos caixas do que objetivos
                min_distancia=sys.maxsize
                for caixa in caixas_disponiveis:
                    d = manhattan(obj,caixa)  # ignoramos possíveis obstáculos
                    if d < min_distancia:
                        min_distancia = d
                        caixa_candidata = caixa
                caixas_disponiveis.remove(caixa_candidata)
                soma_distancias += min_distancia
        sokoban = clone['sokoban']
        max_dist_sokoban_caixa = 0
        for caixa in clone['caixas']:
            if caixa not in self.goal:
                d = manhattan(sokoban,caixa)  # ignoramos possíveis obstáculos
                if d > max_dist_sokoban_caixa:
                    max_dist_sokoban_caixa = d
        return soma_distancias + max_dist_sokoban_caixa
    