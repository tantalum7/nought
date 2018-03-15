
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
        self._size = size

        # Initialise the board matrix to the size specified, filled as empty
        self._matrix = np.matrix(np.full((self._size, self._size), self.EMPTY))

    @property
    def size(self):
        return self._size

    def is_full(self, matrix=None):
        """
        Checks if all board tiles have been taken, and returns true/false
        :param matrix: Optionally apply this to matrix other than the internal one
        :return: bool
        """
        # If matrix is left as None, use the internal board matrix
        matrix = self._matrix if matrix is None else matrix

        # Return true if Board.EMPTY does not appear anywhere in the board (its full)
        return self.EMPTY not in matrix

    def is_won(self, matrix=None):
        """
        Checks for full column, row or diagonal of noughts or crosses.
        :param matrix: Optionally apply this to matrix other than the internal one
        :return: Board.NOUGHT, Board.CROSS or None
        """
        # If matrix is left as None, use the internal board matrix
        matrix = self._matrix if matrix is None else matrix

        # Check rows, and return it if we found a winner
        winner = self._check_rows(matrix)
        if winner:
            return winner

        # Check columns (check rows of transposed matrix), and return it if we found a winner
        winner = self._check_rows(matrix.T)
        if winner:
            return winner

        # Check main diagonal for a winner, and return it if there is one
        winner = self._check_main_diagonal(matrix)
        if winner:
            return winner

        # Check the other diagonal for a winner (flip, then check main diagonal), return the result
        return self._check_main_diagonal(np.fliplr(matrix))

    def is_empty(self, row, col, matrix=None):
        """
        Checks if the tile with row, col specifed is empty or not
        :param row: Row index
        :param col: Column index
        :param matrix: Optionally apply this to matrix other than the internal one
        :return: bool
        """
        # If matrix is left as None, use the internal board matrix
        matrix = self._matrix if matrix is None else matrix

        # Return true if the tile at the given row/col is empty
        return matrix[row, col] == self.EMPTY

    def set_tile(self, row, col, value, matrix=None):
        """
        Sets the tile with the given value
        :param row: Row index
        :param col: Column index
        :param value: Value to set (should be Board.NOUGHT or Board.CROSS)
        :param matrix: Optionally apply this to matrix other than the internal one
        :raises IndexOutOfBoundsException if row/col are out of bounds
        :raises NotEmptyException if tile already taken
        """
        # If matrix is left as None, use the internal board matrix
        matrix = self._matrix if matrix is None else matrix

        # Raise exception if tile isn't empty
        if not self.is_empty(row, col, matrix):
            raise NotEmptyException("row:{}, col:{}".format(row, col))

        # Raise exception if row/col are out of bounds
        if not self._in_bounds(row, col):
            raise IndexOutOfBoundsException("row:{}, col:{} - min:0, max:{}".format(row, col, self._size))

        # Set tile to value
        matrix[row, col] = value

    def matrix_copy(self):
        """
        Returns a copy (unlinked) of the board matrix in its current state. Changes to this matrix do not
        affect the board instance state.
        :return: np.matrix of board state, values are Board.EMPTY, Board.NOUGHT or Board.CROSS
        """
        return self._matrix.copy()

    def list_empty_tiles(self, matrix=None):
        """
        Produces a list of (row, col) tuples of all the empty tiles on the board
        :param matrix: Optionally apply this to matrix other than the internal one
        :return: list of tuples
        """
        rows, cols = np.where(self._matrix == self.EMPTY)
        return [(rows[x], cols[x]) for x in range(len(rows))]


    def _check_rows(self, matrix):
        # Get the number of rows in the matrix
        rows = matrix.shape[0]

        # Iterate through the number of rows
        for row_index in range(rows):

            a = matrix[row_index]
            b = self._row_of(self.NOUGHT)

            # If the row is all noughts, return nought
            if np.array_equal(matrix[row_index], self._row_of(self.NOUGHT)):
                return self.NOUGHT

            # If the row is all crosses, return cross
            elif np.array_equal(matrix[row_index], self._row_of(self.CROSS)):
                return self.CROSS

        # None of the rows are all noughts or crosses, return None
        return None

    def _check_main_diagonal(self, matrix):
        # Check if main diagonal is all noughts
        if np.array_equal(matrix.diagonal(), self._row_of(self.NOUGHT)):
            return self.NOUGHT

        # Check if main diagonal is all crosses
        elif np.array_equal(matrix.diagonal(), self._row_of(self.CROSS)):
            return self.CROSS

        # Main diagonal is not all noughts or crosses, return None
        else:
            return None

    def _row_of(self, val):
        return np.matrix(np.full(self._size, val))

    def _in_bounds(self, row, col):
        return (0 <= row < self._size) or (0 <= col < self._size)

if __name__ == "__main__":


    b = Board(3)

    for x in range(3):
        b.set_tile(x, 0, Board.NOUGHT)

    r = b.is_won()

    a = b.list_empty_tiles()

    pass

