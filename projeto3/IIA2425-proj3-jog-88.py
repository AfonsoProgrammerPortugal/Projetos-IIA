# Grupo: 88
# Membros:
# Afonso Santos - 59808
# Renan Silva - 59802

from tictacchess import *
from utils import *
from jogos import *
# from renan import *
from multiprocessing import Process, Manager
import copy

################################################################
# Funções de avaliação do Afonso
################################################################

# Função que joga o cavalo no centro do tabuleiro
# devolve 1 se o jogador jogar o cavalo no centro
# -1 se o adversário jogar o cavalo no centro
def play_knight_center_88(estado,jogador):
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
def play_bishop_center_88(estado,jogador):
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
def play_rook_corner_88(estado,jogador):
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
def func_opening_moves_88(estado,jogador):
    # Copia o estado para não o alterar
    clone=copy.deepcopy(estado)

    # Verifica se é a primeira jogada
    if clone.n_jogadas == 1 or clone.n_jogadas == 2:
        return play_knight_center_88(clone,jogador)
    elif clone.n_jogadas == 3 or clone.n_jogadas == 4:
        return play_bishop_center_88(clone,jogador)
    elif clone.n_jogadas == 5 or clone.n_jogadas == 6:
        return play_rook_corner_88(clone,jogador)
    else:
        return 0

# Função que verifica se o adversário tem alguma peça que possa
# atacar 3 peças do jogador ou mais
def count_threats_88(estado, pieces, positions):
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
def func_defense_priority_88(estado, jogador):
    # Copia o estado para não o alterar
    clone = copy.deepcopy(estado)

    positions_p1, pieces_p1 = clone.player_used_cells(jogador)
    positions_p2, pieces_p2 = clone.player_used_cells(estado.other())

    if count_threats_88(clone, pieces_p2, positions_p1):
        return 1

    if count_threats_88(clone, pieces_p1, positions_p2):
        return -1

    return 0

# Função que verifica se o jogador tem uma jogada
# que lhe permita ganhar ou quase ganhar o jogo
# devolve 1 se tiver, 0 se não tiver
def winning_move_88(estado,jogador):
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
def func_objective_opportunity_88(estado,jogador):
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

def func_objective_opportunity_other_88(estado,jogador):
    return -func_objective_opportunity_88(estado, estado.other())

# Função que verifica se o jogador pode atacar
def can_attack_positions_88(estado, pieces, positions):
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
def func_attack_priority_88(estado, jogador):
    clone = copy.deepcopy(estado)

    # Verifica se o adversário tem 2 ou 3 na mesma linha
    if func_objective_opportunity_88(clone, clone.other()) == 1:
        pieces_p1 = clone.player_used_pieces(jogador)
        positions_p2, _ = clone.player_used_cells(clone.other())

        # Verifica se o jogador pode atacar
        if can_attack_positions_88(clone, pieces_p1, positions_p2):
            return 1

    elif func_objective_opportunity_88(clone, jogador) == 1:
        pieces_p2 = clone.player_used_pieces(clone.other())
        positions_p1, _ = clone.player_used_cells(jogador)

        if can_attack_positions_88(clone, pieces_p2, positions_p1):
            return -1

    return 0

################################################################
# Funções de avaliação do Renan
################################################################

# defesa e ataque?
#
# 4 em linha
# 3 em linha
# 2 em linha
# numero de pecas
# n de opcoes para cada uma das peças (funções individuais para cada peça)
# player_used_pieces() -> priorizar estados em que o jogador nao tem peao no tab

def how_many_in_line_88(state, player):
    clone = copy.deepcopy(state)
    player_pieces = clone.player_pieces(player)
    player_positions = []

    for piece, pos in clone.board.items():
        if piece in player_pieces:
            player_positions.append(pos)

    best = 0

    for row in range(4):
        local_best = 0
        for col in range(4):
            if (row, col) in player_positions:
                local_best += 1
        if local_best > best:
            best = local_best

    for col in range(4):
        local_best = 0
        for row in range(4):
            if (row, col) in player_positions:
                local_best += 1
        if local_best > best:
            best = local_best

    local_best = 0
    for d in range(4):
        if (d, d) in player_positions:
            local_best += 1
    if local_best > best:
        best = local_best

    local_best = 0
    for d in range(4):
        if (d, 3-d) in player_positions:
            local_best += 1
    if local_best > best:
        best = local_best

    return best


def get_other_player_88(player):
    return 'WHITE' if player == 'BLACK' else 'BLACK'

def function_combine_with_weight_88(state, player, weights, functions, scale):
    return sum([scale * w * f(state, player) for (w, f) in zip(weights, functions)])

def check_n_in_row_88(state, player, n):
    clone = copy.deepcopy(state)

    if n == 4:
        winner = clone.have_winner()

        if winner is not None:
            return infinity if winner == player else -infinity
        return 0
    else:
        result = clone.n_in_row(n)

        if result is None or result == 'BOTH':
            return 0
        return 1 if result == player else -1

def check_if_winner_88(state, player): return check_n_in_row_88(state, player, 4)
def check_3_in_row_88(state, player):  return check_n_in_row_88(state, player, 3)
def check_2_in_row_88(state, player):  return check_n_in_row_88(state, player, 2)

def num_pieces_differential_88(state, player) :
    clone=copy.deepcopy(state)
    n_pieces_player    = len(clone.player_used_pieces(player))
    n_pieces_adversary = len(clone.player_used_pieces(get_other_player_88(player)))

    return n_pieces_player - n_pieces_adversary

def n_valid_piece_options_88(state, player, piece):
    clone = copy.deepcopy(state)
    adversary_squares, _ = clone.player_used_cells(get_other_player_88(player))

    if piece not in clone.used_pieces():
        return 0

    piece_options = list(map(lambda x: x[1], clone.possible_moves(piece)))

    if (player == 'WHITE' and clone.n_capturas[0] == 3) or \
       (player == 'BLACK' and clone.n_capturas[1] == 3):
        for option in piece_options:
            if option in adversary_squares:
                piece_options.remove(option)

    return len(piece_options)

def n_valid_knight_options_88(state, player): return n_valid_piece_options_88(state, player, 'C' if player == 'WHITE' else 'c')
def n_valid_bishop_options_88(state, player): return n_valid_piece_options_88(state, player, 'B' if player == 'WHITE' else 'b')
def n_valid_rook_options_88(state, player):   return n_valid_piece_options_88(state, player, 'T' if player == 'WHITE' else 't')
def n_valid_pawn_options_88(state, player):   return n_valid_piece_options_88(state, player, 'P' if player == 'WHITE' else 'p')

def check_piece_on_board_88(state, player, piece):
    clone = copy.deepcopy(state)
    return 1 if piece in clone.player_used_pieces(player) else -1

def knight_on_board_88(state, player): return check_piece_on_board_88(state, player, 'C' if player == 'WHITE' else 'c')
def bishop_on_board_88(state, player): return check_piece_on_board_88(state, player, 'B' if player == 'WHITE' else 'b')
def rook_on_board_88(state, player):   return check_piece_on_board_88(state, player, 'T' if player == 'WHITE' else 't')
def pawn_on_board_88(state, player):   return check_piece_on_board_88(state, player, 'P' if player == 'WHITE' else 'p')

def adversary_pawn_on_board_88(state, player):
    return pawn_on_board_88(state, 'WHITE' if player == 'BLACK' else 'BLACK')

def check_3_in_row_no_pawn_88(state, player): return 1 if (check_3_in_row_88(state, player) == 1 and \
                                                           pawn_on_board_88(state, player) == -1) else 0

def check_3_in_row_3_pieces_88(state, player):
    clone = copy.deepcopy(state)
    return 1 if (check_3_in_row_88(state, player) == 1 and \
                len(clone.player_used_pieces(player)) == 3) else 0

def two_can_become_three_in_row_88(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line_88(state, player)

    if clone.to_move == player and in_line == 2 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line_88(clone.next_state(move), player) == 3:
                    return 1
    return 0

def can_win_next_move_88(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line_88(state, player)

    if player == clone.to_move and in_line == 3 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line_88(clone.next_state(move), player) == 4:
                    return infinity
    return 0

def adversary_can_win_next_move_88(state, player):
    return can_win_next_move_88(state, get_other_player_88(player))

def can_win_next_next_move_88(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line_88(state, player)

    if player == get_other_player_88(clone.to_move) and in_line == 3 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line_88(clone.next_state(move), player) == 4:
                    return infinity
    return 0

def adversary_can_win_next_next_move_88(state, player):
    return can_win_next_next_move_88(state, get_other_player_88(player))

def can_stop_adversary_win_88(state, player):
    clone = copy.deepcopy(state)

    if (player == clone.to_move) and \
        (adversary_can_win_next_next_move_88(state, player) > 0) and \
        ((clone.n_capturas[0] if player == 'WHITE' else clone.n_capturas[1]) < 3) and \
        (clone.n_jogadas >= 6):
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                next_state = clone.next_state(move)
                if how_many_in_line_88(next_state, get_other_player_88(player)) == 2 or \
                    adversary_can_win_next_move_88(next_state, player) == 0:
                    return 1.5
    return 0

def adversary_can_stop_our_win_88(state, player):
    return can_stop_adversary_win_88(state, get_other_player_88(player))

def can_win_and_adversary_cant_stop_88(state, player):
    return can_win_next_move_88(state, player) and adversary_can_stop_our_win_88(state, player)

def adversary_can_win_and_we_cant_stop_88(state, player):
    return can_win_and_adversary_cant_stop_88(state, get_other_player_88(player))

def can_attack_88(state, player):
    clone = copy.deepcopy(state)

    if clone.n_jogadas >= 6:
        my_counter = 0
        their_counter = 0
        to_move = clone.to_move
        multiplier = 5

        used_pieces = clone.player_used_pieces(player)
        their_positions, _ = clone.player_used_cells(get_other_player_88(player))
        for piece in used_pieces:
            moves = list(map(lambda x: x[1], clone.possible_moves(piece)))
            for move in moves:
                if move in their_positions:
                    my_counter += multiplier if player == to_move else 1

        used_pieces = clone.player_used_pieces(get_other_player_88(player))
        my_positions, _ = clone.player_used_cells(player)

        for piece in used_pieces:
            moves = list(map(lambda x: x[1], clone.possible_moves(piece)))
            for move in moves:
                if move in my_positions:
                    their_counter += multiplier if player == to_move else 1

        return my_counter - their_counter
    else:
        return 0

def can_be_attacked_88(state, player):
    return can_attack_88(state, get_other_player_88(player))

def start_with_knight_center_88(state, player):
    clone = copy.deepcopy(state)

    if clone.n_jogadas <= 6:
        knight = 'C' if player == 'WHITE' else 'c'
        pos, pieces = clone.player_used_cells(player)

        if knight in pieces:
            knight_index = 0
            for index in range(len(pieces)):
                if pieces[index] == knight:
                    knight_index = index
                    break
            row, col = pos[knight_index]
            return 1 if (1 <= row <= 2 and 1 <= col <= 2) else -1
        else:
            return 0
    else:
        return 0

def start_aligning_88(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line_88(state, player)

    if clone.n_jogadas <= 6:
        used_pieces = clone.player_used_pieces(player)

        if (len(used_pieces) == 2 and in_line == 2) or \
           (len(used_pieces) == 3 and in_line == 3):
            return 1
        elif len(used_pieces) == 1:
            return 0
        else:
            return -1
    else:
        return 0

def more_centered_pieces_88(state, player):
    clone = copy.deepcopy(state)

    centered = 0
    border = 0
    pos, pieces = clone.player_used_cells(player)

    for x, y in pos:
        if 1 <= x <= 2 and 1 <= y <= 2:
            centered += 1
        else:
            border += 1

    return centered - border

def in_row_hierarchy_88(state, player):
    res = check_if_winner_88(state, player)
    if res != 0:
        return res

    res1 = can_win_and_adversary_cant_stop_88(state, player)
    res2 = adversary_can_win_and_we_cant_stop_88(state, player)
    if res1 and not res2:
        return 10
    if not res1 and res2:
        return -10

    res1 = can_win_next_move_88(state, player)
    res2 = adversary_can_win_next_move_88(state, player)
    if res1 and not res2:
        return 5
    if not res1 and res2:
        return -5

    res = check_3_in_row_88(state, player)
    if res != 0:
        return res * 2

    res = two_can_become_three_in_row_88(state, player)
    if res:
        return 1

    return 0

def check_how_many_in_line_88(state, player):
    my_result = how_many_in_line_88(state, player)
    their_result = how_many_in_line_88(state, get_other_player_88(player))
    to_move = state.to_move

    if my_result == 4 and their_result < 4:
        return infinity
    if their_result == 4 and my_result < 4:
        return -infinity
    if my_result == 3 and their_result < 3:
        return 2 if to_move == player else 1
    if their_result == 3 and my_result < 3:
        return -1 if to_move == player else -2
    # if my_result == 2 and their_result < 2:
    #     return 1 if to_move == player else 0.5
    # if their_result == 2 and my_result < 2:
    #     return -0.5 if to_move == player else -1
    else:
        return 0
    
################################################################
# Jogadores criados pelos alunos
################################################################

my_combinations = [
    # (check_if_winner_88, 1),
    # (check_3_in_row_88, 1),
    # (check_3_in_row_no_pawn_88, 3),
    # (check_2_in_row_88, 1),
    # (num_pieces_differential_88, 1),
    # (n_valid_knight_options_88, 0.5),
    # (n_valid_bishop_options_88, 0.5),
    # (n_valid_rook_options_88, 0.5),
    # (n_valid_pawn_options_88, 0.5),
    # (knight_on_board_88, 0),
    # (bishop_on_board_88, 0),
    # (rook_on_board_88, 0),
    # (pawn_on_board_88, -1000),
    # (adversary_pawn_on_board_88, 3),
    # (check_3_in_row_3_pieces_88, 2),
    (can_win_next_move_88, 1),
    # (adversary_can_win_next_move_88, -1),
    # (can_stop_adversary_win_88, 1),
    # (adversary_can_stop_our_win_88, -1),
    # (can_win_and_adversary_cant_stop_88, 1),
    # (can_attack_88, 1),
    # (can_be_attacked_88, -1),
    # (func_tactic, 1),
    (check_how_many_in_line_88, 1),
    # (start_with_knight_center_88, 1000),
    # (two_can_become_three_in_row_88, 1),
    # (start_aligning_88, 1),
    # (more_centered_pieces_88, 1),
    # (in_row_hierarchy_88, 1)
    # (func_attack_priority_88, 1),
    # (func_defense_priority_88, 1),
    # (func_objective_opportunity_88, 1),
    # (func_objective_opportunity_other_88, 1)
]

my_functions, my_weights = zip(*my_combinations)

# profundidade
p = 3

def func_88(state, player):
    return function_combine_with_weight_88(state, player, my_weights, my_functions, 1)

def my_player(game, state) :
    # game.display(state)
    # print(state.other())
    # print(state.to_move)
    return alphabeta_cutoff_search_new(state, game,p,eval_fn=func_88)

##############################################################################################################
# Jogador Tactic
##############################################################################################################

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

def jogador_tactic(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,p,eval_fn=func_tactic)
    
################################################################
# Testes
################################################################

jogo = TicTacChess()

def play_n_games(n):
    count = 0

    copy = n

    while copy > 0:
        vencedor = jogo.jogar(my_player, jogador_tactic, verbose=False)
        if vencedor == 1:
            count += 1
        
        print(vencedor)
        copy -= 1
    
    print("Vitórias:", count)

play_n_games(25)

'''num_jogos = 100  # Total de jogos
num_processos = 10  # Número de processos
jogos_por_processo = num_jogos // num_processos  # Jogos que cada processo executará

# Função que cada processo executará
def executar_jogos(resultados_compartilhados, indice):
    vitorias = 0
    for _ in range(5):
        resultado = jogo.jogar(my_player, jogador_tactic, verbose=False)
        print(resultado, end='')
        if resultado == 1:  # Se for uma vitória
            vitorias += 1

    for _ in range(5):
        resultado = jogo.jogar(jogador_tactic, my_player, verbose=False) * -1
        print(resultado, end='')
        if resultado == 1:  # Se for uma vitória
            vitorias += 1
    # Armazena o total de vitórias deste processo na lista compartilhada
    resultados_compartilhados[indice] = vitorias

# Usando Manager para criar uma lista compartilhada
with Manager() as manager:
    resultados_compartilhados = manager.list([0] * num_processos)  # Lista com um espaço para cada processo

    # Criando e iniciando os processos
    processos = []
    for i in range(num_processos):
        processo = Process(target=executar_jogos, args=(resultados_compartilhados, i))
        processos.append(processo)
        processo.start()

    # Aguardando que todos os processos terminem
    for processo in processos:
        processo.join()

    # Calculando a soma total das vitórias
    pontuacao_total = sum(resultados_compartilhados)

print()
print("Pontuação final:", pontuacao_total)'''