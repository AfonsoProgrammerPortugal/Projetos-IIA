from jogos import *
from utils import *
from tictacchess import *
import copy

# defesa e ataque?
#
# 4 em linha
# 3 em linha
# 2 em linha
# numero de pecas
# n de opcoes para cada uma das peças (funções individuais para cada peça)
# player_used_pieces() -> priorizar estados em que o jogador nao tem peao no tab

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

def check_if_winner(state, player):
    return check_n_in_row(state, player, 4)

def check_3_in_row(state, player):
    return check_n_in_row(state, player, 3)

def check_2_in_row(state, player):
    return check_n_in_row(state, player, 2)

def num_pieces_differential(state, _) :
    clone=copy.deepcopy(state)
    n_pieces_player    = len(clone.player_used_pieces(clone.to_move))
    n_pieces_adversary = len(clone.player_used_pieces(clone.other()))

    return n_pieces_player - n_pieces_adversary

def n_valid_piece_options(state, player, piece):
    clone = copy.deepcopy(state)
    adversary_squares, _ = state.player_used_cells(clone.other())

    if piece not in state.board:
        return 0

    piece_options = state.possible_moves(piece)

    if (player == 'WHITE' and state.n_capturas[0] == 3) or \
       (player == 'BLACK' and state.n_capturas[1] == 3):
        for option in piece_options:
            if option in adversary_squares:
                piece_options.remove(option)

    return len(piece_options)

def n_valid_knight_options(state, player):
    return n_valid_piece_options(state, player, 'C' if player == 'WHITE' else 'c')

def n_valid_bishop_options(state, player):
    return n_valid_piece_options(state, player, 'B' if player == 'WHITE' else 'b')

def n_valid_rook_options(state, player):
    return n_valid_piece_options(state, player, 'T' if player == 'WHITE' else 't')

def n_valid_pawn_options(state, player):
    return n_valid_piece_options(state, player, 'P' if player == 'WHITE' else 'p')

def pawn_on_board(state, player):
    clone = copy.deepcopy(state)
    pawn = 'P' if player == 'WHITE' else 'p'

    return 1 if pawn not in clone.player_used_pieces(player) else -1

my_functions = [
    check_if_winner,
    check_3_in_row,
    check_2_in_row,
    num_pieces_differential,
    n_valid_knight_options,
    n_valid_bishop_options,
    n_valid_rook_options,
    n_valid_pawn_options,
    pawn_on_board
]

my_weights = [1,50,5,1,1,1,1,1,5]

def func_renan(state, player):
    return function_combine_with_weight(state, player, my_weights, my_functions, 1)

def my_player(game, state) :
    return alphabeta_cutoff_search_new(state, game,1,eval_fn=func_renan)

###################################

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

def func_pecas(estado,jogador) :
    clone=copy.deepcopy(estado)
    n_pecas_jogador = len(clone.player_used_pieces(clone.to_move))
    n_pecas_adversario = len(clone.player_used_pieces(clone.other()))
    return n_pecas_jogador - n_pecas_adversario

def func_tactic_e_pecas(estado,jogador):
    return func_tactic(estado,jogador) + func_pecas(estado,jogador)

def jogador_tactic_e_pecas(jogo,estado) :
    return alphabeta_cutoff_search_new(estado,jogo,1,eval_fn=func_tactic_e_pecas)




jogo=TicTacChess()

pontuacao=0
for i in range(100):
    resultado = jogo.jogar(my_player,jogador_tactic_e_pecas,verbose=False)
    print(resultado, end = "")
    pontuacao = pontuacao + (1 if resultado == 1 else 0)
print()
print(pontuacao)

# print(jogo.jogar(my_player, jogador_tactic_e_pecas, verbose=False))