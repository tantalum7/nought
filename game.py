
# Libary imports
import random

# Project imports
from board import Board
from player import HumanPlayer, AiPlayer


class Game(object):

    def __init__(self):
        """
        Main game logic class
        """
        # Initialise vars
        self.board = Board(3)
        self._turn_number = 0

        # Initialise list of players, then shuffle it (random player first)
        self.players = [HumanPlayer(self.board), AiPlayer(self.board)]
        random.shuffle(self.players)

    @property
    def turn_number(self):
        return self._turn_number

    @property
    def current_player(self):
        return self.players[self.turn_number % len(self.players)]

    def next_turn(self):
        move = self.current_player.make_move()
        self._turn_number += 1
        return move

    def is_finished(self):
        return self.board.is_won or self.board.is_full
