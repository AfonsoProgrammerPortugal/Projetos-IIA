from tictacchess import *
from utils import *
from jogos import *
import copy

##############################################################################################################
# Conjunto de funções de avaliação dadas no enunciado do projeto
##############################################################################################################
# Variável global que define a profundidade de pesquisa
p=3

# Função que verifica se o jogo terminou e 
# devolve o valor de infinity se o jogador ganhou,
# -infinity se o jogador perdeu e 0 se o jogo ainda não terminou
def func_gameover(estado,jogador) :
    clone=copy.deepcopy(estado) #boa prática de programação, para não arriscarem estragar o estado
    winner = clone.have_winner()
    if winner != None:
        return infinity if winner==jogador else -infinity
    return 0 #em qualquer outra situação que não seja vitória ou derrota

# Função que usa o alphabeta_cutoff_search_new 
# para devolver o melhor movimento para o jogador
# com base na função de avaliação func_gameover
# e com profundidade 1
def jogador_random_plus_1(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,1,eval_fn=func_gameover)

# Função que verifica se o jogador tem três em linha
# e devolve 1 se tiver, -1 se o adversário tiver
# e 0 se ninguém tiver três em linha
def func_tactic(estado,jogador) :
    clone=copy.deepcopy(estado)
    winner = clone.have_winner()
    if winner != None:
        return infinity if winner==jogador else -infinity
    # se não reconhece o final do jogo, verifica quem tem três em linha:
    almost_winner = clone.n_in_row(3)
    if almost_winner == None or almost_winner == 'BOTH':
        return 0
    return 1 if almost_winner==jogador else -1

# Função que usa o alphabeta_cutoff_search_new
# para devolver o melhor movimento para o jogador
# com base na função de avaliação func_gameover
# e com profundidade p
def jogador_random_plus_p(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,p,eval_fn=func_gameover)

# Função que usa o alphabeta_cutoff_search_new
# para devolver o melhor movimento para o jogador
# com base na função de avaliação func_tactic
# e com profundidade p
def jogador_tactic_p(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,p,eval_fn=func_tactic)

# Função que devolve o número de peças do jogador
# menos o número de peças do adversário
def func_pecas(estado,jogador) :
    clone=copy.deepcopy(estado)
    n_pecas_jogador = len(clone.player_used_pieces(clone.to_move))
    n_pecas_adversario = len(clone.player_used_pieces(clone.other()))
    return n_pecas_jogador - n_pecas_adversario

# Função que devolve a combinação linear de func_tactic e func_pecas
def func_tactic_e_pecas(estado,jogador):
    return func_tactic(estado,jogador) + func_pecas(estado,jogador)

# Função que devolve o melhor movimento para o jogador,
# com base na função de avaliação func_tactic_e_pecas
# e com profundidade 3
def jogador_tactic_e_pecas_3(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,3,eval_fn=func_tactic_e_pecas)

# Função que devolve o melhor movimento para o jogador, 
# com base na função de avaliação func_tactic
# e com profundidade 3
def jogador_tactic_3(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,3,eval_fn=func_tactic)

'''jogo=TicTacChess()
jogo.jogar(query_player,jogador_tactic_3) # descomentar para jogar'''

# Função que combina várias funções de avaliação
# com base nos pesos dados
def func_combina_com_pesos(estado,jogador,pesos,funcoes):
    """Função que devolve a combinação linear de várias funções de avaliação."""
    return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])

# Função que devolve a combinação linear de func_tactic e func_pecas
def nova_func_tactic_e_pecas(estado,jogador):
    return func_combina_com_pesos(estado,jogador,[2,0.5],[func_tactic,func_pecas])

# Função que devolve o melhor movimento para o jogador, 
# com base na função de avaliação nova_func_tactic_e_pecas
# e com profundidade 3
def novo_jogador_tactic_e_pecas_3(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,3,eval_fn=nova_func_tactic_e_pecas)

scores={'Vitoria': 3, 'Empate': 1}

# Função que traduz a tabela de resultados em pontos
def traduzPontos(tabela):
    tabelaScore={}
    empates=tabela['Empate']
    for x in tabela:
        if x != 'Empate':
            tabelaScore[x]=scores['Vitoria']*tabela[x]+scores['Empate']*empates
    return tabelaScore

# Função que joga n pares de jogos entre jog1 e jog2
def jogaNpares(jogo,n,jog1,jog2):
    name_jog1=jog1.__name__
    name_jog2=jog2.__name__
    tabelaPrim={name_jog1:0, name_jog2:0, 'Empate':0}
    tabelaSeg={name_jog1:0, name_jog2:0, 'Empate':0}
    tabela={}
    for _ in range(n):
        #_,_,vencedor=jogo.jogar(jog1,jog2,verbose=False)
        vencedor=jogo.jogar(jog1,jog2,verbose=False)
        if vencedor>0:
            vencedor=name_jog1
        elif vencedor<0:
            vencedor=name_jog2
        else:
            vencedor='Empate'
        tabelaPrim[vencedor]+=1
        vencedor=jogo.jogar(jog2,jog1,verbose=False)
        if vencedor>0:
            vencedor=name_jog2
        elif vencedor<0:
            vencedor=name_jog1
        else:
            vencedor='Empate'
        tabelaSeg[vencedor]+=1
    for x in tabelaPrim:
        tabela[x]=tabelaPrim[x]+tabelaSeg[x]
    return tabelaPrim,tabelaSeg,tabela,traduzPontos(tabela)


'''jogo=TicTacChess()
print(jogaNpares(jogo,5,jogador_tactic_e_pecas_3,novo_jogador_tactic_e_pecas_3))
'''

# Função que incorpora os resultados de um torneio
def incorpora(tabela,tx):
    for jog in tx:
        if jog not in tabela:
            tabela[jog]=tx[jog]
        else:
            tabela[jog]+=tx[jog]

# Função que joga um torneio entre n jogadores
def torneio(n,jogadores):
    jogo=TicTacChess()
    tabela={}
    for i in range(len(jogadores)-1):
        jog1=jogadores[i]
        for j in range(i+1,len(jogadores)):
            jog2=jogadores[j]
            print(jog1.__name__,'vs',jog2.__name__)
            _,_,_,tabelaX = jogaNpares(jogo,n,jog1,jog2)
            incorpora(tabela,tabelaX)
    #return tabela
    print(dict(sorted(tabela.items(), key=lambda x: x[1],reverse=True)))

'''torneio(5,[jogador_tactic_3, jogador_tactic_e_pecas_3, novo_jogador_tactic_e_pecas_3])'''