# Grupo: 88
# Membros:
# Afonso Santos - 59808
# Renan Silva - 59802

from tictacchess import *
from utils import *
from jogos import *
import copy

def function_combine_with_weight_88(state, player, weights, functions):
    return sum([w * f(state, player) for (w, f) in zip(weights, functions)])

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
    else:
        return 0


# Função que joga o cavalo no centro do tabuleiro
# devolve 1 se o jogador jogar o cavalo no centro
# -1 se o adversário jogar o cavalo no centro
def play_knight_center_88(estado, jogador):
    piece = "C" if jogador == "WHITE" else "c"
    center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
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
def play_bishop_center_88(estado, jogador):
    piece = "B" if jogador == "WHITE" else "b"
    center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
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
def play_rook_corner_88(estado, jogador):
    piece = "T" if jogador == "WHITE" else "t"
    corner_positions = [(0, 0), (0, 3), (3, 0), (3, 3)]
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
def func_opening_moves_88(estado, jogador):
    # Copia o estado para não o alterar
    clone = copy.deepcopy(estado)

    # Verifica se é a primeira jogada
    if clone.n_jogadas == 0 or clone.n_jogadas == 1:
        return play_knight_center_88(clone, jogador)
    elif clone.n_jogadas == 2 or clone.n_jogadas == 3:
        return play_bishop_center_88(clone, jogador)
    elif clone.n_jogadas == 4 or clone.n_jogadas == 5:
        return play_rook_corner_88(clone, jogador)
    else:
        return 0

my_combinations = [
    (check_how_many_in_line_88, 1),
    (func_opening_moves_88, 1)
]

my_functions, my_weights = zip(*my_combinations)


def func_88(state, player):
    return function_combine_with_weight_88(state, player, my_weights, my_functions)
