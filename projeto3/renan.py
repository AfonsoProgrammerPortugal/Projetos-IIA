from jogos import *
from utils import *
from tictacchess import *
import copy
from multiprocessing import Process, Manager

# defesa e ataque?
#
# 4 em linha
# 3 em linha
# 2 em linha
# numero de pecas
# n de opcoes para cada uma das peças (funções individuais para cada peça)
# player_used_pieces() -> priorizar estados em que o jogador nao tem peao no tab

def how_many_in_line(state, player):
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


def get_other_player(player):
    return 'WHITE' if player == 'BLACK' else 'BLACK'

def function_combine_with_weight(state, player, weights, functions, scale):
    return sum([scale * w * f(state, player) for (w, f) in zip(weights, functions)])

def check_n_in_row(state, player, n):
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

def check_if_winner(state, player): return check_n_in_row(state, player, 4)
def check_3_in_row(state, player):  return check_n_in_row(state, player, 3)
def check_2_in_row(state, player):  return check_n_in_row(state, player, 2)

def num_pieces_differential(state, player) :
    clone=copy.deepcopy(state)
    n_pieces_player    = len(clone.player_used_pieces(player))
    n_pieces_adversary = len(clone.player_used_pieces(get_other_player(player)))

    return n_pieces_player - n_pieces_adversary

def n_valid_piece_options(state, player, piece):
    clone = copy.deepcopy(state)
    adversary_squares, _ = clone.player_used_cells(get_other_player(player))

    if piece not in clone.used_pieces():
        return 0

    piece_options = list(map(lambda x: x[1], clone.possible_moves(piece)))

    if (player == 'WHITE' and clone.n_capturas[0] == 3) or \
       (player == 'BLACK' and clone.n_capturas[1] == 3):
        for option in piece_options:
            if option in adversary_squares:
                piece_options.remove(option)

    return len(piece_options)

def n_valid_knight_options(state, player): return n_valid_piece_options(state, player, 'C' if player == 'WHITE' else 'c')
def n_valid_bishop_options(state, player): return n_valid_piece_options(state, player, 'B' if player == 'WHITE' else 'b')
def n_valid_rook_options(state, player):   return n_valid_piece_options(state, player, 'T' if player == 'WHITE' else 't')
def n_valid_pawn_options(state, player):   return n_valid_piece_options(state, player, 'P' if player == 'WHITE' else 'p')

def check_piece_on_board(state, player, piece):
    clone = copy.deepcopy(state)
    return 1 if piece in clone.player_used_pieces(player) else -1

def knight_on_board(state, player): return check_piece_on_board(state, player, 'C' if player == 'WHITE' else 'c')
def bishop_on_board(state, player): return check_piece_on_board(state, player, 'B' if player == 'WHITE' else 'b')
def rook_on_board(state, player):   return check_piece_on_board(state, player, 'T' if player == 'WHITE' else 't')
def pawn_on_board(state, player):   return check_piece_on_board(state, player, 'P' if player == 'WHITE' else 'p')

def adversary_pawn_on_board(state, player):
    return pawn_on_board(state, 'WHITE' if player == 'BLACK' else 'BLACK')

def check_3_in_row_no_pawn(state, player): return 1 if (check_3_in_row(state, player) == 1 and pawn_on_board(state, player) == -1) else 0

def check_3_in_row_3_pieces(state, player):
    clone = copy.deepcopy(state)
    return 1 if (how_many_in_line(state, player) == 3 and len(clone.player_used_pieces(player)) == 3) else 0

def two_can_become_three_in_row(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line(state, player)

    counter = 0
    if clone.to_move == player and in_line == 2 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line(clone.next_state(move), player) == 3:
                    counter += 1
    return counter

def can_win_next_move(state, player):
    clone = copy.deepcopy(state)
    to_move = clone.to_move
    in_line = how_many_in_line(clone, to_move)

    # print(player == clone.to_move)
    counter = 0
    if in_line == 3 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(to_move)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line(clone.next_state(move), to_move) == 4:
                    counter += 1
    return counter if player == to_move else -counter

def adversary_can_win_next_move(state, player):
    return can_win_next_move(state, get_other_player(player))

def can_win_next_next_move(state, player):
    clone = copy.deepcopy(state)
    in_line = how_many_in_line(state, player)

    counter = 0
    if player == get_other_player(clone.to_move) and in_line == 3 and clone.n_jogadas >= 6:
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                if how_many_in_line(clone.next_state(move), player) == 4:
                    counter += 1
    return counter

def adversary_can_win_next_next_move(state, player):
    return can_win_next_next_move(state, get_other_player(player))

def can_stop_adversary_win(state, player):
    clone = copy.deepcopy(state)

    counter = 0
    if (player == clone.to_move) and (adversary_can_win_next_next_move(state, player) > 0) and (clone.n_jogadas >= 6): #and ((clone.n_capturas[0] if player == 'WHITE' else clone.n_capturas[1]) < 3)
        used_pieces = clone.player_used_pieces(player)
        for piece in used_pieces:
            moves = clone.possible_moves(piece)
            for move in moves:
                next_state = clone.next_state(move)
                if how_many_in_line(next_state, get_other_player(player)) == 2 or adversary_can_win_next_move(next_state, player) == 0:
                    counter += 1
    return counter

def adversary_can_stop_our_win(state, player):
    return can_stop_adversary_win(state, get_other_player(player))

def can_win_and_adversary_cant_stop(state, player):
    return can_win_next_move(state, player) and adversary_can_stop_our_win(state, player)

def adversary_can_win_and_we_cant_stop(state, player):
    return can_win_and_adversary_cant_stop(state, get_other_player(player))

def can_attack(state, player):
    clone = copy.deepcopy(state)

    if clone.n_jogadas >= 6:
        my_counter = 0
        their_counter = 0
        to_move = clone.to_move
        multiplier = 2

        used_pieces = clone.player_used_pieces(player)
        their_positions, _ = clone.player_used_cells(get_other_player(player))
        for piece in used_pieces:
            moves = list(map(lambda x: x[1], clone.possible_moves(piece)))
            for move in moves:
                if move in their_positions:
                    my_counter += multiplier if player == to_move else 1

        used_pieces = clone.player_used_pieces(get_other_player(player))
        my_positions, _ = clone.player_used_cells(player)
        for piece in used_pieces:
            moves = list(map(lambda x: x[1], clone.possible_moves(piece)))
            for move in moves:
                if move in my_positions:
                    their_counter += multiplier if player == to_move else 1

        return my_counter - their_counter
    else:
        return 0

def can_be_attacked(state, player):
    return can_attack(state, get_other_player(player))

def start_with_knight_center(state, player):
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

def start_aligning(state, player):
    if state.n_jogadas <= 6:
        clone = copy.deepcopy(state)
        in_line = how_many_in_line(clone, player)

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

def more_centered_pieces(state, player):
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

def in_row_hierarchy(state, player):
    res = check_if_winner(state, player)
    if res != 0:
        return res

    res1 = can_win_and_adversary_cant_stop(state, player)
    res2 = adversary_can_win_and_we_cant_stop(state, player)
    if res1 and not res2:
        return 10
    if not res1 and res2:
        return -10

    res1 = can_win_next_move(state, player)
    res2 = adversary_can_win_next_move(state, player)
    if res1 and not res2:
        return 5
    if not res1 and res2:
        return -5

    res = check_3_in_row(state, player)
    if res != 0:
        return res * 2

    res = two_can_become_three_in_row(state, player)
    if res:
        return 1

    return 0

def check_how_many_in_line(state, player):
    my_result = how_many_in_line(state, player)
    their_result = how_many_in_line(state, get_other_player(player))
    to_move = state.to_move

    if my_result == 4 and their_result < 4:
        return infinity
    if their_result == 4 and my_result < 4:
        return -infinity
    if my_result == 3 and their_result < 3:
        return 10 if to_move == player else 1
    if their_result == 3 and my_result < 3:
        return -1 if to_move == player else -10
    # if my_result == 2 and their_result < 2:
    #     return 1 if to_move == player else 0.5
    # if their_result == 2 and my_result < 2:
    #     return -0.5 if to_move == player else -1
    else:
        return 0

def func_tactic(estado,jogador) :
    # print(jogador, 123)
    # print(estado.to_move, 444)
    # print(estado.other(), 6667)
    # jogo.display(estado)
    clone=copy.deepcopy(estado)
    winner = clone.have_winner()
    if winner != None:
        return infinity if winner==jogador else -infinity
    # se não reconhece o final do jogo, verifica quem tem três em linha:
    almost_winner = clone.n_in_row(3)
    if almost_winner == None or almost_winner == 'BOTH':
        return 0
    return 1 if almost_winner==jogador else -1

my_combinations = [
    # (check_if_winner, 1),
    # (check_3_in_row, 1),
    # (check_3_in_row_no_pawn, 3),
    # (check_2_in_row, 1),
    # (num_pieces_differential, 1),
    # (n_valid_knight_options, 0.5),
    # (n_valid_bishop_options, 0.5),
    # (n_valid_rook_options, 0.5),
    # (n_valid_pawn_options, 0.5),
    # (knight_on_board, 0),
    # (bishop_on_board, 0),
    # (rook_on_board, 0),
    # (pawn_on_board, 3),
    # (adversary_pawn_on_board, 3),
    # (check_3_in_row_3_pieces, 2),
    # (can_win_next_move, 10),
    # (adversary_can_win_next_move, -5),
    # (can_stop_adversary_win, 5),
    # (adversary_can_stop_our_win, -5),
    # (can_win_and_adversary_cant_stop, 1),
    # (can_attack, 1),
    # (can_be_attacked, -1),
    # (func_tactic, 1),
    (check_how_many_in_line, 1),
    # (two_can_become_three_in_row, 10)
    # (start_with_knight_center, 1),
    # (start_aligning, 1),
    # (more_centered_pieces, 1),
    # (in_row_hierarchy, 1)
]

my_functions, my_weights = zip(*my_combinations)

# profundidade
p = 3

def func_renan(state, player):
    return function_combine_with_weight(state, player, my_weights, my_functions, 1)

def my_player(game, state) :
    # game.display(state)
    # print(state.other())
    # print(state.to_move)
    return alphabeta_cutoff_search_new(state, game,p,eval_fn=func_renan)

###################################

def func_pecas(estado,jogador) :
    clone=copy.deepcopy(estado)
    n_pecas_jogador = len(clone.player_used_pieces(clone.to_move))
    n_pecas_adversario = len(clone.player_used_pieces(clone.other()))
    return n_pecas_jogador - n_pecas_adversario

# def func_tactic_e_pecas(estado,jogador):
#     return func_tactic(estado,jogador) + func_pecas(estado,jogador)

def jogador_tactic(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,p,eval_fn=func_tactic)

########################################################################################################################

jogo = TicTacChess()
# resultado = jogo.jogar(my_player, jogador_tactic, verbose=False)
# print(resultado)
num_jogos = 100  # Total de jogos
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
print("Pontuação final:", pontuacao_total)