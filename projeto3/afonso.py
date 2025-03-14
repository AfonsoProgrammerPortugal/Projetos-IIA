from tictacchess import *
from utils import *
from jogos import *
# from renan import *
from multiprocessing import Process, Manager
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

##############################################################################################################
# Jogador criado por mim
##############################################################################################################

# Função que joga o cavalo no centro do tabuleiro
# devolve 1 se o jogador jogar o cavalo no centro
# -1 se o adversário jogar o cavalo no centro
def play_knight_center(estado,jogador):
    piece = "C" if jogador == "WHITE" else "c"
    center_positions = [(1,1),(1,2),(2,1),(2,2)]
    positions_P1, pieces_P1 = estado.player_used_cells(jogador)
    positions_P2, pieces_P2 = estado.player_used_cells(estado.other())

    for i in range(len(positions_P1)):
        if positions_P1[i] in center_positions and pieces_P1[i] == piece:
            return 1

        elif positions_P2[i] in center_positions and pieces_P2[i] == piece:
            return -1
    
    return 0

# Função que joga o bispo na diagonal oposta ao cavalo
# devolve 1 se o jogador jogar o bispo no centro
# -1 se o adversário jogar o bispo no centro
def play_bishop_center(estado,jogador):
    piece = "B" if jogador == "WHITE" else "b"
    center_positions = [(1,1),(1,2),(2,1),(2,2)]
    positions_P1, pieces_P1 = estado.player_used_cells(jogador)
    positions_P2, pieces_P2 = estado.player_used_cells(estado.other())

    for i in range(len(positions_P1)):
        if positions_P1[i] in center_positions and pieces_P1[i] == piece:
            return 1
        
        elif positions_P2[i] in center_positions and pieces_P2[i] == piece:
            return -1

    return 0

# Função que joga a torre num dos cantos do tabuleiro
# devolve 1 se o jogador jogar a torre num dos cantos
# -1 se o adversário jogar a torre num dos cantos
def play_rook_corner(estado,jogador):
    piece = "T" if jogador == "WHITE" else "t"
    corner_positions = [(0,0),(0,3),(3,0),(3,3)]
    positions_P1, pieces_P1 = estado.player_used_cells(jogador)
    positions_P2, pieces_P2 = estado.player_used_cells(estado.other())

    for i in range(len(positions_P1)):
        if positions_P1[i] in corner_positions and pieces_P1[i] == piece:
            return 1
        
        elif positions_P2[i] in corner_positions and pieces_P2[i] == piece:
            return -1

    return 0

# Funcão que segue a seguinte estratégia nos primeiros 3 movimentos:
# 1. A primeira peça a ser jogada é o cavalo no centro do tabuleiro
# 2. A segunda peça a ser jogada é o bispo na diagonal oposta ao cavalo
# 3. A terceira peça a ser jogada é a torre num dos cantos do tabuleiro
def func_opening_moves(estado,jogador):
    # Copia o estado para não o alterar
    clone=copy.deepcopy(estado)

    # Verifica se é a primeira jogada
    if clone.n_jogadas == 1 or clone.n_jogadas == 2:
        return play_knight_center(clone,jogador)
    elif clone.n_jogadas == 3 or clone.n_jogadas == 4:
        return play_bishop_center(clone,jogador)
    elif clone.n_jogadas == 5 or clone.n_jogadas == 6:
        return play_rook_corner(clone,jogador)
    else:
        return 0

# Função que verifica se o adversário tem alguma peça que possa
# atacar 3 peças do jogador ou mais
def count_threats(estado, pieces, positions):
    for piece in pieces:
        count = 0
        can_move = list(map(lambda x: x[1], estado.possible_moves(piece)))
        for pos in positions:
            if pos in can_move:
                count += 1
        if count > 2:
            return True
    return False

# Função de defesa:
# Verifica se o adversário tem alguma peça que possa
# atacar 3 peças do jogador ou mais
# devolve 1 se tiver, 0 se não tiver
# ou -1 se o jogador pode atacar 3 peças do adversário
def func_defense_priority(estado, jogador):
    # Copia o estado para não o alterar
    clone = copy.deepcopy(estado)

    positions_p1, pieces_p1 = clone.player_used_cells(jogador)
    positions_p2, pieces_p2 = clone.player_used_cells(estado.other())

    if count_threats(clone, pieces_p2, positions_p1):
        return 1

    if count_threats(clone, pieces_p1, positions_p2):
        return -1

    return 0

# Função que verifica se o jogador tem uma jogada
# que lhe permita ganhar ou quase ganhar o jogo
# devolve 1 se tiver, 0 se não tiver
def winning_move(estado,jogador):
    # Copia o estado para não o alterar
    clone=copy.deepcopy(estado)
    _ ,pieces = clone.player_used_cells(jogador)

    for piece in pieces:
        moves = estado.possible_moves(piece)
        for move in moves:
            possible_win = clone.next_state(move)
            # Verifica se o jogador aumenta a sua linha
            if (clone.n_in_row(2) == jogador and possible_win.n_in_row(3) == jogador) or \
               (clone.n_in_row(3) == jogador and possible_win.n_in_row(4) == jogador):
                return 1
        
    return 0


# Funcão de objetivo:
# verifica se o jogador tem 2 ou 3 peças
# na mesma linha, coluna ou diagonal
# e tem uma peça livre que possa ser jogada
# para continuar a linha, coluna ou diagonal
# devolve 1 se tiver, 0 se não tiver
def func_objective_opportunity(estado,jogador):
    # Copia o estado para não o alterar
    clone=copy.deepcopy(estado)

    # Verifica se o jogador tem 3 na mesma linha
    # e se tem uma peça livre que possa ser jogada
    if clone.n_in_row(3) == jogador:
        return infinity
    
    # Verifica se o jogador tem 2 na mesma linha
    # e se tem uma peça livre que possa ser jogada
    elif clone.n_in_row(2) == jogador:
        return 1

    else:
        return 0    

def func_objective_opportunity_other(estado,jogador):
    return -func_objective_opportunity(estado, estado.other())

# Função que verifica se o jogador pode atacar
def can_attack_positions(estado, pieces, positions):
    for piece in pieces:
        can_move = list(map(lambda x: x[1], estado.possible_moves(piece)))
        for pos in positions:
            if pos in can_move:
                return True
    return False

# Função de ataque: 
# Verifica se o adversário tem 2 ou 3 peças
# na mesma linha, coluna ou diagonal
# e tem uma peça livre que possa ser jogada
# para atacar essas peças
# devolve 1 se o adversário, 0 se não tiver
# ou -1 se eu tiver 2 ou 3 peças 
def func_attack_priority(estado, jogador):
    clone = copy.deepcopy(estado)

    # Verifica se o adversário tem 2 ou 3 na mesma linha
    if func_objective_opportunity(clone, clone.other()) == 1:
        pieces_p1 = clone.player_used_pieces(jogador)
        positions_p2, _ = clone.player_used_cells(clone.other())

        # Verifica se o jogador pode atacar
        if can_attack_positions(clone, pieces_p1, positions_p2):
            return 1

    elif func_objective_opportunity(clone, jogador) == 1:
        pieces_p2 = clone.player_used_pieces(clone.other())
        positions_p1, _ = clone.player_used_cells(jogador)

        if can_attack_positions(clone, pieces_p2, positions_p1):
            return -1

    return 0

# Função com os pesos e funções de avaliação do jogador criado por mim
def func_afonso(estado,jogador):
    # copia o estado para não o alterar
    clone=copy.deepcopy(estado) 

    # Caso seja o inicio do jogo
    if clone.n_jogadas <= 6:
        return func_opening_moves(clone,jogador)
    # Caso seja o meio do jogo
    else:
        my_functions = [
            func_attack_priority,
            func_defense_priority,
            func_objective_opportunity,
            func_objective_opportunity_other,
            func_tactic
        ]
        my_weights = [100, 50, 100000, 100000, 1]

        return func_combina_com_pesos(clone,jogador,my_weights,my_functions)


# Função com o jogador criado por mim
def my_player2(game, state) :
    return alphabeta_cutoff_search_new(state, game,p,eval_fn=func_afonso)

##############################################################################################################
# Testes
##############################################################################################################

jogo = TicTacChess()

# Função que joga n jogo entre o jogador criado por mim e um jogador aleatório
def play_n_games(n):
    count = 0

    copy = n

    while copy > 0:
        vencedor = jogo.jogar(my_player2, jogador_tactic_p, verbose=False)
        if vencedor == 1:
            count += 1
        
        print(vencedor)
        copy -= 1
    
    print("Vitórias:", count)

play_n_games(25)
