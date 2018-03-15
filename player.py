
# Library imports
import random

# Project imports
from board import IndexOutOfBoundsException, NotEmptyException


class Player(object):

    def __init__(self, board, name, is_nought):
        """
        Generic player class. Do not use directly, instead use class that inherits this
        such as HumanPlayer or AiPlayer.
        :param board: ref to game's Board instance
        :param name: Name of the player
        :param is_nought: Playing as noughts?
        """
        self._board = board
        self.name = name
        self._is_nought = is_nought
        self._set_val = self._board.NOUGHT if is_nought else self._board.CROSS

    @property
    def is_nought(self):
        return self._is_nought

    @property
    def noughts_or_crosses_string(self):
        return "noughts" if self.is_nought else "crosses"

    def set_tile(self, row, col):
        self._board.set_tile(row, col, self._set_val)


class HumanPlayer(Player):

    def __init__(self, board, is_nought, name="Human"):
        super(HumanPlayer, self).__init__(board=board, is_nought=is_nought, name=name)

    def make_move(self):

        # Loop forever (or until a valid move is made)
        while True:

            # Ask user for a move
            user_str = raw_input("Enter move, human (row col)")
            user_inputs = user_str.strip(" ").split(" ")

            # If the user response doesn't split into two values, tell them to try again
            if len(user_inputs) != 2:
                print("Parse error. Try again, stupid human.")

            # We have two values (of questionable nature)
            else:
                # Try to parse the user_inputs as row/col ints, and make the move
                try:
                    row = int(user_inputs[0])
                    col = int(user_inputs[1])
                    self.set_tile(row, col)

                # Catch value error (not a number), and tell user to try again
                except ValueError:
                    print("That's not an integer number. Try again, stupid human.")

                # Catch index out of range, and tell user to try again
                except IndexOutOfBoundsException:
                    print("Tile index out of range. Try again, stupid human.")

                # Catch tile not empty, and tell user to try again
                except NotEmptyException:
                    print("Tile is already taken. Try again, stupid human.")

                # Valid move made, lets break the loop
                else:
                    break


class AiPlayer(Player):

    RANDOM_ALGORITHM = 0
    RANDOM_DEFENSIVE_ALGORITHM = 1

    def __init__(self, board, is_nought, name="HAL9000", algorithm=RANDOM_ALGORITHM):
        super(AiPlayer, self).__init__(board=board, is_nought=is_nought, name=name)
        self._algorithm_choice = algorithm
        self._algorithms = {self.RANDOM_ALGORITHM: self._random_algorithm,
                            self.RANDOM_DEFENSIVE_ALGORITHM: self._random_defensive_algorithm}

    def make_move(self):
        self._algorithms[self._algorithm_choice]()

    def _random_algorithm(self):

        # Loop forever (or until a valid move is found)
        while True:

            # Get random tile row/col position
            row = random.randrange(0, self._board.size)
            col = random.randrange(0, self._board.size)

            # Try to make the random move
            try:
                self.set_tile(row, col)

            # Catch not empty exception, and ignore
            except NotEmptyException:
                pass

            # We found a valid move, break the loop
            else:
                break

        # Return the move
        return row, col

    def _random_defensive_algorithm(self):

        # If the enemy is one move away from winning, take that tile
        enemy_winning_move = self._find_enemy_winning_move()
        if enemy_winning_move:
            self.set_tile(*enemy_winning_move)
            return enemy_winning_move

        # Enemy isn't one tile from wining, just take a random tile
        else:
            return self._random_algorithm()

    def _find_enemy_winning_move(self):

        # Fetch the enemy player type (if we're noughts, they must be crosses)
        enemy = self._board.CROSS if self.is_nought else self._board.NOUGHT

        # Iterate through all empty tiles
        for row, col in self._board.list_empty_tiles():

            # Grab a clean copy of the board matrix
            matrix = self._board.matrix_copy()

            # Set the tile as an enemy tile
            self._board.set_tile(row, col, enemy, matrix)

            # Can the enemy now win?
            if self._board.is_won(matrix) == enemy:
                return (row, col)

        # If we get here, the enemy is not one turn away from winning, return None
        return None

