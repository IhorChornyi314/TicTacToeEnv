import numpy as np


class Board:
    @property
    def size(self):
        return self._size

    @property
    def board(self):
        return self._board

    def __str__(self):
        # use numpy's array representation as basis (a bit of a hack but whatever)
        board_str = ' ' + str(self._board)
        cleaned_up_board_str = board_str.replace('[', '').replace(']', '').replace('  ', ' ')
        return cleaned_up_board_str.replace('-1', 'O').replace('1', 'X').replace('0', '_')

    def __init__(self, size):
        if size <= 0:
            raise ValueError('Size of the board must by a natural number')
        self._size = size
        # board is represented by an array of values: 0 for empty, 1 for crosses and -1 for noughts
        self._board = np.zeros((size, size), dtype='int')
        self.game_ended = False

    def get_legal_moves(self):
        # create action mask
        result = np.ones((self._size, self._size), dtype='int')
        return result - np.abs(self._board)

    def check_for_end_of_game(self, move):
        # we only need to check places impacted by the move

        # check if board is full
        if np.sum(np.abs(self._board)) == self._size * self._size:
            return True

        # check row
        if np.abs(np.sum(self._board[move[0]])) == self._size:
            return True

        # check column
        if np.abs(np.sum(self._board.T[move[1]])) == self._size:
            return True

        # check diagonals
        if move[0] == move[1] and np.abs(np.sum(np.diagonal(self._board))) == self._size:
            return True
        if move[0] + move[1] == self._size - 1 and np.abs(np.sum(np.diagonal(np.fliplr(self._board)))) == self._size:
            return True

        return False

    def add_move(self, move):
        # check for game ended
        if self.game_ended:
            return False, True
        # ensure move legality
        if self._board[move[0], move[1]] != 0:
            raise ValueError('Illegal move made!')
        # change board condition
        self._board[move[0], move[1]] = move[2]
        self.game_ended = self.check_for_end_of_game(move)
        return self.game_ended and np.sum(np.abs(self._board)) != self._size * self._size, self.game_ended

    def reset(self):
        self._board = np.zeros((self._size, self._size), dtype='int')







