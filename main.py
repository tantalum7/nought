
# Library imports
from game import Game


def main():


    while True:

        # Initialise game
        game = Game()

        # Print player info
        print("First player is {}, using noughts".format(game.players[0].name))
        print("Second player is {}, using crosses".format(game.players[1].name))

        # Wait for user to be ready
        raw_input("Press any key to start")

        # Initial game render
        game.render()

        # Loop until game finishes
        while not game.is_finished():
            game.next_turn()
            game.render()

        # Fetch winner, and print winner name or draw if there is no winner
        winner = game.winning_player
        if winner:
            print("Game over. Winner is {}".format(winner.name))
        else:
            print("Game over. Its a draw, how exciting.")

        # Ask if the user wants to play again
        raw_input("Press any key to play again...")


if __name__ == "__main__":

    main()







