
# Project imports
import numpy as np


class IndexOutOfBoundsException(Exception): pass
class NotEmptyException(Exception): pass

class Board(object):

    EMPTY = 0
    NOUGHT = 1
    CROSS = 2

    def __init__(self, size=3):
        """
        Class to store the current state of the noughts&crosses board, with a user defined square size
        :param size:
        """
        # Store board size in class (size == width == height)
        self._size = 3

        # Initialise the board matrix to the size specified, filled as empty
        self._matrix = np.matrix(np.full((self._size, self._size), self.EMPTY))

    @property
    def matrix(self):
        """
        Returns a copy (unlinked) of the board matrix in its current state. Changes to this matrix do not
        affect the board instance state.
        :return: np.matrix of board state, values are Board.EMPTY, Board.NOUGHT or Board.CROSS
        """
        return self._matrix.copy()

    @property
    def size(self):
        return self._size

    def is_full(self):
        """
        Checks if all board tiles have been taken, and returns true/false
        :return: bool
        """
        return self.EMPTY not in self._matrix

    def is_won(self):
        """
        Checks for full column, row or diagonal of noughts or crosses.
        :return: Board.NOUGHT, Board.CROSS or None
        """
        # Check rows, and return it if we found a winner
        winner = self._check_rows(self._matrix)
        if winner:
            return winner

        # Check columns (check rows of transposed matrix), and return it if we found a winner
        winner = self._check_rows(self._matrix.T)
        if winner:
            return winner

        # Check main diagonal for a winner, and return it if there is one
        winner = self._check_main_diagonal(self._matrix)
        if winner:
            return winner

        # Check the other diagonal for a winner (flip, then check main diagonal), return the result
        return self._check_main_diagonal(np.fliplr(self._matrix))

    def is_empty(self, row, col):
        """
        Checks if the tile with row, col specifed is empty or not
        :param row: Row index
        :param col: Column index
        :return: bool
        """
        return self._matrix[row, col] == self.EMPTY

    def set_tile(self, row, col, value):
        """
        Sets the tile with the given value
        :param row: Row index
        :param col: Column index
        :param value: Value to set (should be Board.NOUGHT or Board.CROSS)
        :raises IndexOutOfBoundsException if row/col are out of bounds
        :raises NotEmptyException if tile already taken
        """
        # Raise exception if tile isn't empty
        if not self.is_empty(row, col):
            raise NotEmptyException("row:{}, col:{}".format(row, col))

        # Raise exception if row/col are out of bounds
        if not self._in_bounds(row, col):
            raise IndexOutOfBoundsException("row:{}, col:{} - min:0, max:{}".format(row, col, self._size))

        # Set tile to value
        self._matrix[row, col] = value

    def _check_rows(self, matrix):
        # Get the number of rows in the matrix
        rows = matrix.shape[0]

        # Iterate through the number of rows
        for row_index in range(rows):

            # If the row is all noughts, return nought
            if self._matrix[row_index] == self._row_of(self.NOUGHT):
                return self.NOUGHT

            # If the row is all crosses, return cross
            elif self._matrix[row_index] == self._row_of(self.CROSS):
                return self.CROSS

        # None of the rows are all noughts or crosses, return None
        return None

    def _check_main_diagonal(self, matrix):
        # Check if main diagonal is all noughts
        if matrix.diagonal() == self._row_of(self.NOUGHT):
            return self.NOUGHT

        # Check if main diagonal is all crosses
        elif matrix.diagonal() == self._row_of(self.CROSS):
            return self.CROSS

        # Main diagonal is not all noughts or crosses, return None
        else:
            return None

    def _row_of(self, val):
        return np.matrix(np.full(self._size, val))

    def _in_bounds(self, row, col):
        return (0 > row > self._size) or (0 > col > self._size)
