
# Libary imports
import random

# Project imports
from board import Board
from player import HumanPlayer, AiPlayer
from view import View

class Game(object):

    def __init__(self, size=3):
        """
        Main game logic class
        """
        # Initialise vars
        self.board = Board(size)
        self.view = View(self.board)
        self._turn_number = 0

        # Initialise players
        self.nought_player = HumanPlayer(self.board, True)
        self.cross_player = AiPlayer(self.board, False)
        self.players = [self.nought_player, self.cross_player]

        # Shuffle player list to randomise first player
        random.shuffle(self.players)

    @property
    def turn_number(self):
        return self._turn_number

    @property
    def current_player(self):
        return self.players[self.turn_number % len(self.players)]

    @property
    def winning_player(self):
        if self.board.is_won() == Board.NOUGHT:
            return self.nought_player
        elif self.board.is_won() == Board.CROSS:
            return self.cross_player
        else:
            return None

    def next_turn(self):
        move = self.current_player.make_move()
        self._turn_number += 1
        return move

    def is_finished(self):
        return self.board.is_won() or self.board.is_full()

    def render(self):
        self.view.render()



if __name__ == "__main__":

    game = Game()

    game.render()

    print("done")
    pass