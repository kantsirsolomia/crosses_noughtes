import copy
import random
from linkedbst import *
from bstnode import *


def generate_winning_combinations():
    combinations = []
    for i in range(3):
        combination1 = []
        combination2 = []
        for j in range(3):
            combination1.append((i, j))
            combination2.append((j, i))
        combinations.append(combination1)
        combinations.append(combination2)

    combinations.append([(0, 0), (1, 1), (2, 2)])
    combinations.append([(0, 2), (1, 1), (2, 0)])
    return combinations


class Board:
    NOUGHT = 1
    CROSS = -1
    EMPTY = 0

    NOUGHT_WINNER = 1
    CROSS_WINNER = -1
    DRAW = 2
    NOT_FINISHED = 0

    WINNING_COMBINATIONS = generate_winning_combinations()

    def __init__(self):
        self.cells = [[0] * 3 for _ in range(3)]
        self.last_move = Board.NOUGHT
        self.number_of_moves = 0
        self.last_position = (0, 0)

    def make_move(self, cell):  # by Oles' Dobosevych
        '''
        Makes a move on the board.
        '''
        if self.cells[cell[0]][cell[1]] != self.EMPTY:
            return False
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def has_winner(self, board):  # by Oles' Dobosevych
        '''
        Checks if board has a winner.
        '''
        for combination in self.WINNING_COMBINATIONS:
            lst = []
            for cell in combination:
                lst.append(board[cell[0]][cell[1]])
            if max(lst) == min(lst) and max(lst) != Board.EMPTY:
                return max(lst)
        if self.number_of_moves == 9:
            return Board.DRAW

        return Board.NOT_FINISHED

    def make_random_move(self):  # by Oles' Dobosevych
        '''
        Makes a random move on the board.
        '''
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == Board.EMPTY:
                    possible_moves.append((i, j))
        cell = random.choice(possible_moves)
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def game_tree(self):  # by me
        '''
        Makes a recursive binary tree with play boards as branches.
        '''
        tree = LinkedBST()
        tree.add(self.cells)
        self.computer = False

        if self.last_move == Board.NOUGHT:
            self.computer = False
        elif self.last_symbol == self.CROSS:
            self.computer = True

        def recurse(branch):

            if self.computer == True:
                current_symbol = self.NOUGHT
            else:
                current_symbol = self.CROSS

            while True:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
                if self.cells[x][y] == self.EMPTY:
                    self.last_move = current_symbol
                    break

            if self.has_winner(branch.data) != Board.NOT_FINISHED or self.has_winner(branch.data) != Board.DRAW:
                return 'done'
            board_right = copy.deepcopy(branch.data)
            self.make_move(
                (self.last_position[0], self.last_position[1]))

            branch.right = BSTNode(board_right)

            while True:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
                if self.cells[x][y] == self.EMPTY:
                    self.last_position = current_symbol
                    break

            if self.has_winner(branch.data) != Board.NOT_FINISHED or self.has_winner(branch.data) != Board.DRAW:
                return 'done'
            board_left = copy.deepcopy(branch.data)
            self.make_move(
                (self.last_position[0], self.last_position[1]))

            branch.left = BSTNode(board_left)
            recurse(branch.right)
            recurse(branch.left)
        recurse(tree._root)
        return tree

    def compute_score(self):  # by Oles' Dobosevych
        '''
        Calculates a score.
        '''
        has_winner = self.has_winner(self.cells)
        if has_winner:
            winner_scores = {Board.NOUGHT_WINNER: 1,
                             Board.CROSS_WINNER: -1, Board.DRAW: 0}
            return winner_scores[has_winner]
        left_board = copy.deepcopy(self)
        right_board = copy.deepcopy(self)
        left_board.make_random_move()
        right_board.make_random_move()
        return left_board.compute_score() + right_board.compute_score()

    def __str__(self):  # by me
        '''
        String output.
        '''
        out = ''
        for pos in self.cells:
            for pos1 in pos:
                if pos1 == None:
                    out += '  '
                else:
                    out += str(pos1)
            out += '\n'
        return out

    # def __str__(self):
    #     transform = {'0': " ", 1: "O", -1: "X"}
    #     return "\n".join([" ".join(map(lambda x: transform[x], row)) for row in self.cells])


if __name__ == "__main__":
    board1 = Board()
    board1.make_random_move()
    board2 = Board()
    board2.make_random_move()
    print(board1)
    print(board1.compute_score())
    print(board2)
    print(board2.compute_score())
    print(board1.game_tree())
    print(board1.compute_score())
