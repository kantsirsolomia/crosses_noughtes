from board_1 import *


def game():
    board = Board()

    while True:
        print(board.choose_pos())
        if board.last_move == board.NOUGHT:
            if Board.compute_score(board) == board.CROSS_WINNER:
                print("computer wins")
            elif Board.compute_score(board) == board.NOUGHT_WINNER:
                print("user wins")
                break
            board.last_move = board.CROSS

        row = int(input('Enter row: '))
        col = int(input('Enter col: '))
        if board.make_move([row, col]) == False:

            while board.make_move([row, col]) == False:
                row = int(input('Enter row: '))
                col = int(input('Enter col: '))
                try:
                    board.make_move([row, col])
                except IndexError:
                    print('This cell is out of range.')
        else:
            try:
                board.make_move([row, col])
            except IndexError:
                print('This cell is out of range.')

        if Board.compute_score(board) == board.CROSS_WINNER:
            print("computer wins")
        elif Board.compute_score(board) == board.NOUGHT_WINNER:
            print("user wins")
            break
        board.last_move = board.NOUGHT
        print(board)


game()
