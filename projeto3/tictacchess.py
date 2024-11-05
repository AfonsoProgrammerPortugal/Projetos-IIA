from jogos import *
from itertools import combinations


def in_row(cells):
    if is_diagonal(cells) or is_line(cells):
        return True
    else:
        return False
        
def is_diagonal(coords):
    x0, y0 = coords[0]
    x1, y1 = coords[1]
    if y1 - y0 == 0:
        return False
    else:
        slope = (x1 - x0) / (y1 - y0)
    for (x, y) in coords[2:]:
        if (y - y0 == 0) or ((x - x0) / (y - y0) != slope):
            return False
    return True
    
def is_line(coords):
    x0, y0 = coords[0]
    if all(x == x0 for x, y in coords) or all(y == y0 for x, y in coords):
        return True
    else:
        return False

    
MAX_JOGADAS = 500

stateTicTacChess = namedtuple('stateTicTacChess', 'to_move, board, n_jogadas, n_capturas, pawn_direction, last_piece')

class EstadoTicTacChess(stateTicTacChess):
    
    def player_pieces(self,player):
        """Returns all symbols used for the pieces of player"""
        return {'C', 'B', 'T', 'P'} if player == 'WHITE' else {'c', 'b', 't', 'p'}
    
    def used_pieces(self):
        """Returns all used pieces"""
        return self.board.keys()
    
    def player_used_pieces(self,player):
        """Returns all used pieces of player"""
        return [piece for piece in self.used_pieces() if piece in self.player_pieces(player)]
    
    def player_used_cells(self,player):
        """Returns all used cells and pieces of player"""
        pieces = self.player_used_pieces(player)
        squares = [self.board[key] for key in pieces]
        return squares, pieces
    
    def empty_cells(self,state):
        """Returns all empty cells"""
        return [(x,y) for x in range(self.h) for y in range(self.v) if (x,y) not in self.board.values()]
    
    def next_state(self,action):
        """Execute action from self (state). Put piece in square replacing whatever was there (maybe nothing).
        If pawn entered board, movement is forward. If there was a capture, increment counter. Increment n_jogadas."""
        board = self.board.copy()
        n_capturas = self.n_capturas
        pawn_direction = self.pawn_direction
        piece, loc = action
        # se a peça é um peão, se está no final do tabuleiro inverte a direção:
        if piece == 'P' or piece == 'p':
            if piece == 'P' and loc[0] == 0:
                pawn_direction[0] = -1 * pawn_direction[0]
            if piece == 'p' and loc[0] == self.v - 1:
                pawn_direction[1] = -1 * pawn_direction[1]
        # se temos nova captura, incrementa contador:
        if loc in self.board.values():
            if self.to_move == 'WHITE':
                n_capturas[0] += 1
            else:
                n_capturas[1] += 1
        # se não temos nova captura, faz reset ao contador:
        else:
            if self.to_move == 'WHITE':
                n_capturas[0] = 0
            else:
                n_capturas[1] = 0
        # só agora coloca peça no tabuleiro (removendo alguma que estivesse nessa casa):
        captured_piece = next((key for key, value in board.items() if value == loc), None)
        if captured_piece != None:
            del board[captured_piece]
            # se um peão foi capturado a sua direção fica +1 por defeito:
            if captured_piece == 'P':
                pawn_direction[0] = 1
            else:
                if captured_piece == 'p':
                    pawn_direction[1] = 1
        board[piece] = loc
        # incrementa número de jogadas e última peça jogada:
        n_jogadas = self.n_jogadas + 1
        last_piece = piece
        return EstadoTicTacChess(to_move=self.other(),board=board,n_jogadas=n_jogadas,n_capturas=n_capturas,pawn_direction=pawn_direction,last_piece=last_piece)
    
    def possible_moves(self,piece):
        loc = self.board[piece]
        if piece == 'C' or piece == 'c':
            list_moves = self.knight_possible_moves(loc)      
        if piece == 'B' or piece == 'b':
            directions = [(+1,+1),(+1,-1),(-1,+1),(-1,-1)]
            list_moves = self.bishop_rook_possible_moves(loc,directions)
        if piece == 'T' or piece == 't':
            directions = [(+1,0),(-1,0),(0,+1),(0,-1)]
            list_moves = self.bishop_rook_possible_moves(loc,directions)
        if piece == 'P' or piece =='p': 
            list_moves = self.pawn_possible_moves(piece,loc)
        list_moves = [(piece,mov) for mov in list_moves]   
        return list_moves
    
    def knight_possible_moves(self,loc):
        # list all new locations based on piece behavior:
        deltas = [(+1,+2),(+1,-2),(-1,+2),(-1,-2),(+2,+1),(+2,-1),(-2,+1),(-2,-1)]
        movements = [(loc[0]+delta[0], loc[1]+delta[1]) for delta in deltas]
        # filter out the locations outside the board:
        movements = [(x,y) for (x,y) in movements if x in range(self.h) and y in range(self.v)]
        # filter out the locations on top of own's pieces:
        my_cells,_ = self.player_used_cells(self.to_move)
        movements = [(x,y) for (x,y) in movements if (x,y) not in my_cells]
        return movements
    
    def bishop_rook_possible_moves(self,loc,directions):
        movements = []
        # list all new locations on all directions still within the board:
        for delta in directions:
            x = loc[0] + delta[0]
            y = loc[1] + delta[1]
            while x in range(self.h) and y in range(self.v):
                if (x,y) in self.board.values():
                    opponent_cells,_ = self.player_used_cells(self.other())
                    if (x,y) in opponent_cells:
                        movements.append((x,y))
                    break
                else:
                    movements.append((x,y))
                    x += delta[0]
                    y += delta[1]
        return movements
    
    def pawn_possible_moves(self,piece,loc):
        # list all new locations based on piece behavior:
        # (need to know which direction (+1 or -1) the pawn is moving, and whether there are opponents in possible new locs)
        if piece == 'P': # to_move is WHITE
            new_straight_loc = (loc[0]-self.pawn_direction[0],loc[1])
            new_diagonal_loc1 = (loc[0]-self.pawn_direction[0],loc[1]+1)
            new_diagonal_loc2 = (loc[0]-self.pawn_direction[0],loc[1]-1)
        else:
            new_straight_loc = (loc[0]+self.pawn_direction[0],loc[1])
            new_diagonal_loc1 = (loc[0]+self.pawn_direction[0],loc[1]+1)
            new_diagonal_loc2 = (loc[0]+self.pawn_direction[0],loc[1]-1)           
        movements = []
        if new_straight_loc not in self.board.values(): # pawn can only move if no one is blocking it
            movements.append(new_straight_loc)
        opponent_cells, opponent_pieces = self.player_used_cells(self.other())
        if new_diagonal_loc1 in opponent_cells: # pawn can move diagonally to take an opponent's piece
            movements.append(new_diagonal_loc1) 
        if new_diagonal_loc2 in opponent_cells:
            movements.append(new_diagonal_loc2) 
        # filter out the locations outside the board:
        movements = [(x,y) for (x,y) in movements if x in range(self.h) and y in range(self.v)]
        return movements
        
    def n_in_row(self,n):
        "Return the player or players who have n-in-row (maybe Both), or None."
        #(play,board,jogadas,capturas,pawn_direction,piece)=self
        if self.last_piece=="None":
            return None
        cells1,_ = self.player_used_cells(self.to_move)
        cells2,_ = self.player_used_cells(self.other())
        if len(cells1) < n and len(cells2) < n:
            return None     
        who_has = None
        if len(cells1) == n:
            cells1 = sorted(cells1)
            if in_row(cells1):
                who_has = self.to_move
        else:
            if len(cells1) > n: # we check if a group of them is in_row, assume
                for group_cells1 in combinations(cells1, n):
                    group_cells1 = sorted(group_cells1)
                    if in_row(group_cells1):
                        who_has = self.to_move
                        break
        if len(cells2) == n:
            cells2 = sorted(cells2)
            if in_row(cells2):
                if who_has == None:
                    who_has = self.other()
                else:
                    who_has = 'BOTH'
        else:
            if len(cells2) > n: # we check if a group of them is in_row
                for group_cells2 in combinations(cells2, n):
                    group_cells2 = sorted(group_cells2)
                    if in_row(group_cells2):
                        if who_has == None:
                            who_has = self.other()
                        else:
                            who_has = 'BOTH'
        return who_has

    def other(self):
        """Who is the other, the one that is not the next to move"""
        return 'BLACK' if self.to_move == 'WHITE' else 'WHITE'
    
    def have_winner(self):
        return self.n_in_row(4)
            
    def display(self,h,v):
        """Display the state given the number of lines and columns"""
        board_items = self.board.items()
        print('   ',end='')
        for y in range(v):
            print('__', end='')
        print('_')
        for x in range(h):
            print(x, '|', end=' ')
            for y in range(v):
                piece = next((key for key, value in board_items if value == (x,y)), '.')
                print(piece, end=' ')
            print('|', end=' ')
            print()
        print('  |',end='')
        for x in range(v):
            print('__', end='')
        print('_|')
        print('    ',end='')
        for y in range(h):
            print(y, end=' ')
        print()
        

class TicTacChess(Game):
    """Play Tic Tac Chess on an h x v board (h is the height of the board, and v the width), with first player being 'WHITE'.
    A state has: the player to move; a board in the form of a dictionary of {Piece: Location} entries, number of turns done so far,
    number of consecutive captures by WHITE and BLACK, pawn direction of WHITE and BLACK, and last piece played."""

    def __init__(self, h=4, v=4):
        "The board is empty, it is 'WHITE' that begins, no captures, normal pawn direction, no last piece"
        self.h = 4
        self.v = 4
        self.initial = EstadoTicTacChess(to_move='WHITE',board={},n_jogadas=0,n_capturas=[0,0],pawn_direction=[1,1],last_piece='None')
        EstadoTicTacChess.h=4
        EstadoTicTacChess.v=4

    def actions(self, state):
        """List of legal actions are any valid piece movements of player to_move, either placing them on empty squares or moving them on
        the board. Moving pieces is allowed only after the first 6 pieces are on the board. Moving pieces can capture opponent's pieces."""
        # actions can be the placement of new pieces (on empty squares):
        list_actions = []
        my_pieces = state.player_pieces(state.to_move)
        stock = [piece for piece in my_pieces if piece not in state.used_pieces()] # pieces that player (to_move) has in stock
        for piece in stock:
            empty = state.empty_cells(state)
            for square in empty:
                list_actions.append((piece,square))
        # after 6 pieces on the board, actions can also be movements (anywhere except on top of my pieces):
        if state.n_jogadas >= 6: 
            my_used_pieces = state.player_used_pieces(state.to_move)
            for piece in my_used_pieces:
                piece_possible_movements = state.possible_moves(piece)
                # if number of consecutive captures is 3, another capture is forbidden (which means no movements to used cells):
                if (state.to_move == 'WHITE' and state.n_capturas[0] == 3) or (state.to_move == 'BLACK' and state.n_capturas[1] == 3):
                    piece_possible_movements = [mov for mov in piece_possible_movements if mov not in state.board.values()]
                list_actions.extend(piece_possible_movements)
        #print(list_actions)
        return list_actions

    def result(self, state, action):
        "Execute action from state, returning next state"
        return state.next_state(action)
        
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if state.n_jogadas == MAX_JOGADAS:
            return 0
        return 1 if player != state.to_move else -1 # != porque entretanto o to_move já mudou para o outro
    
    def terminal_test(self, state):
        """A state is terminal if one of the players has 4 pieces in a row or if MAX_JOGADAS is reached."""
        return True if state.n_in_row(4) != None or state.n_jogadas == MAX_JOGADAS else False
        
    def display(self, state):
        is_final = self.terminal_test(state);
        print("   Jogadas feitas:", state.n_jogadas)
        if not(is_final):
            print("   Tabuleiro atual:")
        else:
            print("   Tabuleiro final:")
        state.display(self.h,self.v)
        if not(is_final):
            print("   Próximo jogador:", state.to_move)
            # o que os jogadores têm em stock:
            if state.to_move == 'WHITE':
                stock_w = [piece for piece in state.player_pieces(state.to_move) if piece not in state.player_used_pieces(state.to_move)]
                stock_b = [piece for piece in state.player_pieces(state.other()) if piece not in state.player_used_pieces(state.other())]
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Stock de peças:", str(stock_w), "(black: " ,str(stock_b), ")"))
            else:
                stock_b = [piece for piece in state.player_pieces(state.to_move) if piece not in state.player_used_pieces(state.to_move)]
                stock_w = [piece for piece in state.player_pieces(state.other()) if piece not in state.player_used_pieces(state.other())]
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Stock de peças:", str(stock_b), "(white: " ,str(stock_w), ")"))
            # estatísticas do jogo:
            if state.to_move == 'WHITE':
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Capturas seguidas:", state.n_capturas[0], "(black: " ,state.n_capturas[1], ")"))
            else:
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Capturas seguidas:", state.n_capturas[1], "(white: " ,state.n_capturas[0], ")"))
            # para que lado se move o peão (mesmo que ainda não esteja lá):
            if state.pawn_direction[0] == 1:
                mov_w = 'normal'
            else:
                mov_w = 'inverso'
            if state.pawn_direction[1] == 1:
                mov_b = 'normal'
            else:
                mov_b = 'inverso'
            if state.to_move == 'WHITE':
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Movimento do peão:", mov_w, "(black: " ,mov_b, ")\n"))
            else:
                print("{:<25}{:<24}{:<8}{:<20}{:<1}".format("      Movimento do peão:", mov_b, "(white: " ,mov_w, ")\n"))
        else:
            player1_won = self.utility(state,'WHITE')
            print("   \nFIM do jogo")
            if player1_won > 0:
                print('   Ganhou WHITE')
            elif player1_won < 0:
                print('   Ganhou BLACK')
            else:
                print('   Empate ao fim de', MAX_JOGADAS, 'jogadas!')
            print()