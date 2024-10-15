from searchPlus import *

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


linha1= "  #####\n"
linha2= "###...#\n"
linha3= "#o@$..#\n"
linha4= "###.$o#\n"
linha5= "#o##..#\n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9


class Sokoban(Problem):
    """O """
    
    dict_actions = {'N': (-1,0), 'W': (0,-1), 'E': (0,1), 'S': (1,0)}

    def __init__(self, initial=None,goal=None,situacaoInicial=mundoStandard):
        """A partir do puzzle em txt geramos um dicionários de onde extráimos:
        * o estado, as posições objectivo, as casas bavegáveis, o mapa e as paredes.
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
        
    def possible(self,sokoban,caixas,deltas):
        l,c=sokoban
        #print('sokoban:',(l,c))
        dl,dc=deltas
        #print('deltas:',(dl,dc))
        l1,c1=l+dl,c+dc
        #print('next:',(l1,c1),'In caixas?',(l1,c1) in caixas,'In navegáveis?',(l1,c1) in self.navegaveis)
        if not (l1,c1) in caixas:
            #print('sai na primeira')
            return (l1,c1) in self.navegaveis
        else:
            #print('sai no else')
            l2,c2=l1+dl,c1+dc
            #print('nextnext:',(l2,c2),'In caixas?',(l2,c2) in caixas,'In navegáveis?',(l2,c2) in self.navegaveis)
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
                #print(cel,viz,(l+dl,c+dc))
            if num_viz > 2:
                #print(False)
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
        return [action for action in self.dict_actions if self.possible(sokoban,state['caixas'],self.dict_actions[action])]
    
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

    def h_inutil_1(self, node):
        """Heurística inútil pois só reconhece estados finais e, caso contrário,
        devolve a distância de Manhattan entre o Sokoban e a caixa mais distante."""
        clone=copy.deepcopy(node.state)
        ## Satisfaz objectivo?
        if self.goal_test(clone):
            return 0
        max_distancia_sokoban = 0
        sokoban = clone['sokoban']
        for caixa in clone['caixas']:
            d_sokoban = manhattan(sokoban,caixa)  # ignoramos possíveis obstáculos
            if d_sokoban > max_distancia_sokoban:
                max_distancia_sokoban = d_sokoban
        return max_distancia_sokoban
    
    def h_inutil_2(self, node):
        """Heurística inútil pois só conta quantas caixas falta arrumar nos lugares de armazenamento."""
        clone=copy.deepcopy(node.state)
        ## Satisfaz objectivo?
        if self.goal_test(clone):
            return 0
        n_caixas_desarrumadas = len(clone['caixas'])
        for caixa in clone['caixas']:
            if caixa in self.goal:
                n_caixas_desarrumadas -= 1
        return n_caixas_desarrumadas
