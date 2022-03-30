import random
from copy import copy, deepcopy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    number_of_placed_coins = 0

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.number_of_placed_coins < 8

        if not drop_phase:

            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            pass

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []

        val, row, col, src_row, src_col = self.minimax(state, 6 , float("-inf"), float("inf"), True)
        self.number_of_placed_coins += 1
        # (row, col) = (random.randint(0,4), random.randint(0,4))
        # while not state[row][col] == ' ':
        #     (row, col) = (random.randint(0,4), random.randint(0,4))
        # ensure the destination (row,col) tuple is at the beginning of the move list

        move.insert(0, (row, col))
        if src_row != -1:
            move.append((src_row, src_col))

        self.number_of_placed_coins += 1
        return move

    def heuristic_game_value(self, state, piece):

        def hhr(state, piece):

            value = 0
            boardWeights = [
                [0, 1, 0, 1, 0],
                [1, 2, 2, 2, 1],
                [0, 2, 3, 2, 0],
                [1, 2, 2, 2, 1],
                [0, 1, 0, 1, 0]
            ]
            for x in range(5):
                for y in range(5):
                    if state[x][y]  == piece:
                        value = value + boardWeights[x][y]
            return value

        ai = hhr(state, self.my_piece)
        op = hhr(state, self.opp)

        # print(state)
        return 1 if ai > op else -1

    def isLegal(self, x, y, state):
        return 0 <= x < 5 and 0 <= y < 5 and state[x][y] == ' '

    def minimax(self, state, depth, alpha, beta, maximisingPlayer):

        game_value = self.game_value(state)

        # # if game value = 0, then it will exit in main itself right
        if game_value != 0:
            # return a legit move here ... why i dont think its needed ... since dest loop takes care of it
            return (game_value, -1, -1,-1,-1)

        if depth == 0:
            # return
            return (self.heuristic_game_value(state,  self.my_piece if maximisingPlayer else self.opp), -1, -1,-1,-1)

        deep_copy_state = deepcopy(state)

        dest_row, dest_col = -1, - 1

        if maximisingPlayer:
            source_row = -1
            source_col = -1

            if self.number_of_placed_coins < 8:
                for i in range(len(deep_copy_state)):
                    for j in range(len(deep_copy_state[0])):
                        if deep_copy_state[i][j] == ' ':
                            deep_copy_state[i][j] = self.my_piece
                            self.number_of_placed_coins += 1
                            child_val, r, c,r2,c2 = self.minimax(deep_copy_state , depth - 1, alpha, beta, not maximisingPlayer)
                            if child_val > alpha:
                                alpha = child_val
                                dest_row = i
                                dest_col = j
                                if alpha >= beta:
                                    # print("pruned")
                                    deep_copy_state[i][j] = ' '
                                    self.number_of_placed_coins -= 1
                                    return (beta, dest_row, dest_col, -1, -1)
                            deep_copy_state[i][j] = ' '
                            self.number_of_placed_coins -= 1
            else:

                sources = []

                for i in range(len(deep_copy_state)):
                    for j in range(len(deep_copy_state[0])):
                        if deep_copy_state[i][j] == self.my_piece:
                            sources.append([i,j])

                for row, col in sources:
                    dir_r = [-1,0,1]
                    dir_c = [-1,0,1]

                    for dirr in dir_r:
                        for dirc in dir_c:
                            if self.isLegal(row+dirr, col+dirc, state):
                                deep_copy_state[row][col],deep_copy_state[row+dirr][col+dirc] = deep_copy_state[row+dirr][col+dirc], deep_copy_state[row][col]
                                child_val, r, c, r2,c2 = self.minimax(deep_copy_state, depth - 1, alpha, beta,
                                                               not maximisingPlayer)
                                if child_val > alpha:
                                    # print("camer here")
                                    alpha = child_val
                                    dest_row = row+dirr
                                    dest_col = col+dirc
                                    source_row = row
                                    source_col = col
                                    if alpha >= beta:
                                        # print("pruned")
                                        return (beta, dest_row, dest_col, source_row, source_col)

                                deep_copy_state[row + dirr][col + dirc], deep_copy_state[row][col] = \
                                deep_copy_state[row][col], deep_copy_state[row + dirr][col + dirc]

            return (alpha, dest_row, dest_col, source_row, source_col)

        else:
            dest_row = -1
            dest_col = -1
            source_row = -1
            source_col = -1
            m = float("inf")
            if self.number_of_placed_coins < 8:
                for i in range(len(deep_copy_state)):
                    for j in range(len(deep_copy_state[0])):
                        if deep_copy_state[i][j] == ' ':
                            deep_copy_state[i][j] = self.opp
                            self.number_of_placed_coins += 1
                            child_val, r, c,r2,c2 = self.minimax(deep_copy_state, depth - 1, alpha, beta, not maximisingPlayer)
                            if child_val < beta:
                                beta = child_val
                                dest_row = i
                                minmax_col = j # why is this minimax_col ?
                            if alpha >= beta:
                                # print("pruned")
                                self.number_of_placed_coins -= 1
                                deep_copy_state[i][j] = ' '
                                return (alpha, dest_row, minmax_col, -1, -1)

                            # TODO should we move this inside the pruned if statement too?
                            self.number_of_placed_coins -= 1
                            deep_copy_state[i][j] = ' '
            else:
                sources = []
                for i in range(len(deep_copy_state)):
                    for j in range(len(deep_copy_state[0])):
                        if deep_copy_state[i][j] == self.my_piece:
                            sources.append([i, j])

                for row, col in sources:
                    dir_r = [-1, 0, 1]
                    dir_c = [-1, 0, 1]

                    for dirr in dir_r:
                        for dirc in dir_c:
                            if self.isLegal(row + dirr, col + dirc, state):
                                deep_copy_state[row][col], deep_copy_state[row + dirr][col + dirc] = \
                                deep_copy_state[row + dirr][col + dirc], deep_copy_state[row][col]
                                child_val, r, c,r2,c2 = self.minimax(deep_copy_state, depth - 1, alpha, beta,
                                                               not maximisingPlayer)
                                if child_val < beta:
                                    beta = child_val
                                    dest_row = row + dirr
                                    dest_col = col + dirc
                                    source_row = row
                                    source_col = col

                                if alpha >= beta:
                                    return (alpha, dest_row, dest_col, source_row, source_col)

                                deep_copy_state[row + dirr][col + dirc], deep_copy_state[row][col] = \
                                    deep_copy_state[row][col], deep_copy_state[row + dirr][col + dirc]

        return (beta, dest_row, dest_col, source_row, source_col)


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # Check \ diagonal wins
        for i in range(2):
            for j in range(2):
                cur_st = state[i][j]
                win = True
                for pos in range(4):
                    # (i+pos, j+pos)
                    if state[i + pos][j + pos] == ' ' or state[i + pos][j + pos] != cur_st:
                        win = False
                        break
                if win:
                    return 1 if cur_st == self.my_piece else -1

        # Check / diagonal wins
        for i in range(2):
            for j in range(2):
                cur_st = state[i][4 - j]
                win = True
                for pos in range(4):
                    # (i+pos, 4-j-pos)
                    if state[i + pos][4 - j - pos] == ' ' or state[i + pos][4 - j - pos] != cur_st:
                        win = False
                        break
                if win:
                    return 1 if cur_st == self.my_piece else -1

        # Check diamond wins using centers
        for i in range(1, 4):
            for j in range(1, 4):
                if state[i][j] == ' ' and state[i][j + 1] != ' ' and state[i][j + 1] == state[i][j - 1] == \
                        state[i + 1][j] == state[i - 1][j]:
                    return 1 if state[i][j + 1] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            # ai.place_piece([1,1], ai.my_piece)
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
