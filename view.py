

class View(object):

    def __init__(self, board):
        """
        Simple ascii text based view, to display the current board state
        :param board:
        """
        self._board = board

    def render(self):
        """
        Render the current board state to the screen, in ascii text
        """

        # Grab a copy of the board matrix
        board_matrix = self._board.matrix_copy()

        # Clear the console screen
        self.clear_screen()

        # Print the initial line col numbers
        print("     "+"  ".join([str(x) for x in range(self._board.size)]))

        # Iterate through each row
        for row in range(self._board.size):

            # Prepare a string with the row number
            row_str = " {} ".format(row)

            # Iterate through each column
            for col in range(self._board.size):

                # Set the appropriate icon char if the tile is nought, cross or empty
                if board_matrix[row, col] == self._board.NOUGHT:
                    icon = "0"
                elif board_matrix[row, col] == self._board.CROSS:
                    icon = "X"
                else:
                    icon = "."

                # Append icon to row string
                row_str += "  " + icon

            # Now we've finished concating the row string, print it
            print(row_str)

    def clear_screen(self):
        """
        Clear the screen, by printing loads of newlines
        """
        print('\n' * 80)
