#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible"]
__version__ = "0.1.0"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


import tkinter as tk
import Worawich_590PZ_spot
import spot_AI

""" YEEEEEEEEELLOOOOOOOOOWW TUUUUUUUUUURNNN ISSSSS 0000000000000000000000"""

class GamePlay(object):

    def __init__(self, board_size=5, num_player=2, board=None, turn=0, score=None):
        self.EDGE_SIZE = board_size  # move horizontal
        self.history = []
        if board is None:
            self.board = [[-1 for y in range(self.EDGE_SIZE)] for x in range(self.EDGE_SIZE)]
            self.init_board()

        else:
            self.board = board.copy()
        if score is None:
            self.score = 0, 0
        else:
            self.score = self.count_total_score()
        self.turn = turn
        # self.game_complete = 0
        self.num_player = num_player
        # self.GameBoard = Worawich_590PZ_spot.GameBoard(Worawich_590PZ_spot.frame)


    def show_board(self):
        for x in self.board:
            print(x)

    def init_board(self):
        self.board[0][0] = 1
        self.board[self.EDGE_SIZE -1][self.EDGE_SIZE -1] = 1
        self.board[self.EDGE_SIZE -1][0] = 0
        self.board[0][self.EDGE_SIZE -1] = 0

    # def set_board_size(self):
    #     GamePlay.__init__.EDGE_SIZE = int(input("Set up board size of ?x?: "))
    #     GamePlay.__init__.board = [[-1 for y in range(self.EDGE_SIZE)] for x in range(self.EDGE_SIZE)]

    def is_game_complete(self) -> bool:
        print("Check completion")
        if self.count_total_score()[0] == 0 or self.count_total_score()[1] == 0:
            print("DEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            return True
        for j in self.board:
            for i in j:
                if i == -1:
                    print("NOT COMPLETEE", self.board)
                    return False
        print("DEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")

        return True

    def is_empty_spot(self, x, y):
        if (self.board[y][x]) == -1:
            return True
        return False

    def get_empty_walk(self, x, y):
        empty_list = []

        #  Offset calculation system, so it find only the spots with index within range 3
        upper_offset_y = 0
        if ((y + 1) + 1) / self.EDGE_SIZE > 1:
            upper_offset_y = (((y + 1) + 1) - self.EDGE_SIZE)  # y+1 make it true number +upper space need -board size
            # print("upper_offset_y", upper_offset_y)
        upper_offset_x = 0
        if ((x + 1) + 1) / self.EDGE_SIZE > 1:
            upper_offset_x = (((x + 1) + 1) - self.EDGE_SIZE)  # x+1 make it true number +upper space need -board size
            # print("upper_offset_x", upper_offset_x)
        lower_offset_y = 0
        if (y - 1) < 0:
            lower_offset_y = (y - 1)  # y -lower space need
            # print("lower_offset_y", lower_offset_y)
        lower_offset_x = 0
        if (x - 1) < 0:
            lower_offset_x = (x - 1)  # x -lower space need
            # print("lower_offset_x", lower_offset_x)

        for i in range(3 - upper_offset_x + lower_offset_x):
            for j in range(3 - upper_offset_y + lower_offset_y):
                if self.board[y + (j - 1) - lower_offset_y][x + (i - 1) - lower_offset_x] == -1:
                    empty_list.append((x + (i - 1) - lower_offset_x, y + (j - 1) - lower_offset_y))
        return empty_list

    def get_empty_jump(self, x, y):
        empty_list = []

        #  Offset calculation system, to find the jumping region without going over boarder edge.
        upper_offset_y = 0
        if ((y + 1) + 2)/self.EDGE_SIZE > 1:
            upper_offset_y = (((y + 1) + 2) - self.EDGE_SIZE)  # y+1 make it true number +upper space need -board size
            # print("upper_offset_y", upper_offset_y)
        upper_offset_x = 0
        if ((x + 1) + 2)/self.EDGE_SIZE > 1:
            upper_offset_x = (((x + 1) + 2) - self.EDGE_SIZE)  # x+1 make it true number +upper space need -board size
            # print("upper_offset_x", upper_offset_x)
        lower_offset_y = 0
        if (y - 2) < 0:
            lower_offset_y = (y - 2)  # y -lower space need
            # print("lower_offset_y", lower_offset_y)
        lower_offset_x = 0
        if (x - 2) < 0:
            lower_offset_x = (x - 2)  # x -lower space need
            # print("lower_offset_x", lower_offset_x)

        # Loop through the 5x5 jumping region minus the edge offset
        for i in range(5 - upper_offset_x + lower_offset_x):
            for j in range(5 - upper_offset_y + lower_offset_y):
                if self.board[y+(j-2)-lower_offset_y][x+(i-2)-lower_offset_x] == -1:
                    empty_list.append((x+(i-2)-lower_offset_x, y+(j-2)-lower_offset_y))

        # Remove the inner 3x3 to get the frame only
        for space in self.get_empty_walk(x, y):
            empty_list.remove(space)
        return empty_list

    def get_empty_around(self, x, y, board=None):
        """Same with above but contain both 3x3 and 5x5 space. AKA all legal move"""
        if board is None:
            board = self.board
        else:
            board = board
        empty_list = []

        #  Offset calculation system, to find the jumping region without going over boarder edge.
        upper_offset_y = 0
        if ((y + 1) + 2)/self.EDGE_SIZE > 1:
            upper_offset_y = (((y + 1) + 2) - self.EDGE_SIZE)  # y+1 make it true number +upper space need -board size
            # print("upper_offset_y", upper_offset_y)
        upper_offset_x = 0
        if ((x + 1) + 2)/self.EDGE_SIZE > 1:
            upper_offset_x = (((x + 1) + 2) - self.EDGE_SIZE)  # x+1 make it true number +upper space need -board size
            # print("upper_offset_x", upper_offset_x)
        lower_offset_y = 0
        if (y - 2) < 0:
            lower_offset_y = (y - 2)  # y -lower space need
            # print("lower_offset_y", lower_offset_y)
        lower_offset_x = 0
        if (x - 2) < 0:
            lower_offset_x = (x - 2)  # x -lower space need
            # print("lower_offset_x", lower_offset_x)

        # Loop through the 5x5 jumping region minus the edge offset
        for i in range(5 - upper_offset_x + lower_offset_x):
            for j in range(5 - upper_offset_y + lower_offset_y):
                if board[y+(j-2)-lower_offset_y][x+(i-2)-lower_offset_x] == -1:
                    empty_list.append((x+(i-2)-lower_offset_x, y+(j-2)-lower_offset_y))
        return empty_list

    def picking_the_piece_legal(self, x, y):
        if self.board[y][x] == self.turn:
            return True
        else:
            return False

    def moving_the_piece_legal(self, x, y, x2, y2):
        if (x2, y2) in self.get_empty_around(x, y):
            return True
        else:
            return False

    def is_move_legal(self, x, y, x2, y2) -> bool:
        ''' Checking on click.  '''
        return self.moving_the_piece_legal(x, y, x2, y2)

    def determine_move_type(self, x, y, x2, y2):
        if (x2, y2) in self.get_empty_walk(x, y):
            return 'walk'
        elif (x2, y2) in self.get_empty_jump(x, y):
            return 'jump'

    def get_game_state(self):
        return self.turn

    def get_history(self):
        return self.history

    def make_history(self, x, y, x2, y2):
        self.history.append([x, y, x2, y2])
        return self.history

    # def remove_history(self, x, y):
    #     self.history.append([self.current_turn, x, y])
    #     return self.history

    def update_board(self, x, y):
        self.board[y][x] = self.turn
        return

    def remove_move_on_board(self, x, y):
        self.board[y][x] = -1
        return

    def determine_next_player(self):
        if GamePlay().turn == 1:
            return "yellow"
        elif GamePlay().turn == 0:
            return "blue"

    def current_turn(self):
        return self.turn

    def whose_turn(self):
        if GamePlay().turn == 1:
            return "blue"
        else:
            return "yellow"

    def make_move(self, x, y, x2, y2, turn=None):
        self.make_history(x, y, x2, y2)
        # self.last_move = [x, y, x2, y2]
        # print("Movinggggggggggggggggggg ", x, y, x2, y2)

        # if turn is None:
        #     turn = self.turn
        # else:
        #     turn = turn
        # print(self.last_move)
        if self.picking_the_piece_legal(x, y):
            if self.moving_the_piece_legal(x, y, x2, y2):
                print("Moving: ", x, y, x2, y2)
                # self.last_move = [x, y, x2, y2]
                # print(self.get_history())
                if self.determine_move_type(x, y, x2, y2) == 'walk':
                    self.board[y2][x2] = self.board[y][x]
                elif self.determine_move_type(x, y, x2, y2) == 'jump':
                    self.board[y2][x2] = self.board[y][x]
                    self.board[y][x] = -1
        self.score = self.count_total_score()
        self.turn = (self.turn + 1) % 2

    def copy_move(self, move):
        print("Copy move: ", move)
        b = self.copy()
        print("Cloned board: ", b.board)
        b.make_move(move[0], move[1], move[2], move[3])
        print("Cloned board moved: ", b.board)
        # b.last_move = move
        return b

    def copy(self):
        '''Returns a deep-copy of the board.'''
        return GamePlay(board=self.board, turn=self.turn, score=self.score)

    def invade(self, x, y):
        oppo_list = []

        #  Offset calculation system, so it find only the spots with index within range 3
        upper_offset_y = 0
        if ((y + 1) + 1) / self.EDGE_SIZE > 1:
            upper_offset_y = (((y + 1) + 1) - self.EDGE_SIZE)  # y+1 make it true number +upper space need -board size
            # print("upper_offset_y", upper_offset_y)
        upper_offset_x = 0
        if ((x + 1) + 1) / self.EDGE_SIZE > 1:
            upper_offset_x = (((x + 1) + 1) - self.EDGE_SIZE)  # x+1 make it true number +upper space need -board size
            # print("upper_offset_x", upper_offset_x)
        lower_offset_y = 0
        if (y - 1) < 0:
            lower_offset_y = (y - 1)  # y -lower space need
            # print("lower_offset_y", lower_offset_y)
        lower_offset_x = 0
        if (x - 1) < 0:
            lower_offset_x = (x - 1)  # x -lower space need
            # print("lower_offset_x", lower_offset_x)

        for i in range(3 - upper_offset_x + lower_offset_x):
            for j in range(3 - upper_offset_y + lower_offset_y):
                opponent = (self.turn + 1) % 2
                if self.board[y + (j - 1) - lower_offset_y][x + (i - 1) - lower_offset_x] == opponent:
                    self.board[y + (j - 1) - lower_offset_y][x + (i - 1) - lower_offset_x] = self.turn
                    oppo_list.append((x + (i - 1) - lower_offset_x, y + (j - 1) - lower_offset_y))
        return oppo_list

    def get_possible_move(self, turn=None, board=None):
        if board is None:
            board = self.board
        else:
            board = board

        if turn is None:
            turn = self.turn
        else:
            turn = turn

        move_list = []
        for i in range(self.EDGE_SIZE): # x
            for j in range(self.EDGE_SIZE): # y
                if board[j][i] == turn:
                    movable = self.get_empty_around(i, j, board)
                    for move in movable:
                        move_list.append([i, j, move[0], move[1]])
        return move_list

    def count_total_score(self, board=None):
        player0, player1 = 0, 0

        if board is not None:
            for row in range(self.EDGE_SIZE):
                player0 += board[row].count(0)
                player1 += board[row].count(1)
            return player0, player1

        for row in range(self.EDGE_SIZE):
            player0 += self.board[row].count(0)
            player1 += self.board[row].count(1)
        return player0, player1

    def count_my_score(self):
        player0 = 0
        for row in range(self.EDGE_SIZE):
            player0 += self.board[row].count(0)
        return player0

    def who_won(self):
        print("WHO WONNNNNNNNNNNNNN??????")
        if self.count_total_score().index(max(self.count_total_score())) == 0:
            return "Yellow"
        else:
            return "Blue"  # Need to change to color variable


    def get_last_move(self):
        # return self.GameBoard.x, self.GameBoard.y, self.GameBoard.x2, self.GameBoard.y2
        print("Last move:", self.history[-1])
        return self.history[-1]

import argparse
import random
import tkinter as tk
import Worawich_590PZ_spot
import spot_AI

def run_random():
    while not game.is_game_complete():
        game.show_board()
        pos_move = game.get_possible_move()
        ran_move = random.choice(pos_move)
        game.make_move(ran_move[0], ran_move[1], ran_move[2], ran_move[3])
        print(game.get_history())
        print(game.get_last_move())
        print("***************************")
    print("Game over.\nBoard:")
    game.show_board()
    print("\nPlayer 0:", game.count_total_score()[0], "\nPlayer 1:", game.count_total_score()[1], )


def run_ai():

    parser = argparse.ArgumentParser(description='4-connect')
    parser.add_argument('--player', type=int, default=0, help='Player to play with - 0 starts.')
    parser.add_argument('--depth', type=int, default=5, help='AI lookahead depth')
    args = parser.parse_args()

    AI = spot_AI.AI(game, player=((args.player + 1) % 2), max_depth=args.depth)
    while not game.is_game_complete():
        if args.player == 0:
            print(args.player)
            print("RANNNNNNNNNDOMMMMMMMMM")
            ran_move = random.choice(game.get_possible_move())
            game.make_move(ran_move[0], ran_move[1], ran_move[2], ran_move[3], args.player)
            args.player = (args.player + 1) % 2

        else:
            print(args.player)
            print("AIIIIIIIIIIIIII")
            AI.move(args.player)
            args.player = (args.player + 1) % 2

        print(game.is_game_complete(), "*#########################################################***")

        print(args.player)
        # game.tuen = (game.turn + 1) % 2
        print("***************************")


from sys import float_info


def run_max_ai():
    turn = 0
    while not game.is_game_complete():
        game.show_board()
        if turn == 0:
            ran_move = random.choice(game.get_possible_move())
            game.make_move(ran_move[0], ran_move[1], ran_move[2], ran_move[3], turn)
            turn = (turn + 1) % 2
        else:
            best = (-float_info.max, None)

            # ran_move = random.choice(game.get_possible_move())
            for move in game.get_possible_move():
                if game.count_total_score(game.copy_move(move).board)[turn] > best[0]:
                    best = game.count_total_score(game.copy_move(move).board)[turn], move
            game.make_move(best[1][0], best[1][1], best[1][2], best[1][3], turn)
            turn = (turn + 1) % 2


class sim_ai:
    def __init__(self):
        last_move = None


    def run_simple_ai(self):
        turn = 0
        while not game.is_game_complete():
            game.show_board()
            if turn == 0:
                ran_move = random.choice(game.get_possible_move())
                game.make_move(ran_move[0], ran_move[1], ran_move[2], ran_move[3], turn)
                turn = (turn + 1) % 2
            else:
                self.move_simple_ai(turn)
                turn = (turn + 1) % 2


    def move_simple_ai(self, turn):
        best = self.simple_ai(game, 0, True, turn)
        print("best", best)
        game.make_move(best[1][0], best[1][1], best[1][2], best[1][3], turn)

    def simple_ai(self, board, depth, maximizing_player, turn):
        if self.last_move is not None:
            if depth == 0 or game.is_game_complete():
                return game.count_total_score(game.copy_move(self.last_move).board)[turn], self.last_move

        if maximizing_player:
            max_eval = -float_info.max
            for self.move in game.get_possible_move(turn):
                eval = self.simple_ai(game.copy_move(self.move), depth - 1, False, turn)
                if eval[0] > max_eval:
                    max_eval = eval
                    self.last_move = self.move
                # max_eval = max(max_eval, eval)
            # turn = (turn + 1) % 2
            return max_eval, self.move

        else:
            min_eval = float_info.max
            for self.move in game.get_possible_move((turn + 1)% 2):
                eval = self.simple_ai(game.copy_move(self.move), depth - 1, False, turn)
                if eval[0] < min_eval:
                    min_eval = eval
                    self.last_move = self.move
                min_eval = min(min_eval, eval)
            # turn = (turn + 1) % 2
            return min_eval, self.move

if __name__ == '__main__':
    game = GamePlay(5)
    game.init_board()
    game.show_board()

    run_ai()  # Look at get_possible_move and duplicated board
    # run_random()
    # run_max_ai()
    # sim_ai().run_simple_ai()

    # print(game.is_game_complete())
    # print(game.is_empty_spot(2, 3))

    # # Finding legal move spots
    # # middle spot
    # print(game.get_empty_walk(2, 3))
    # # lower corner spot
    # print(game.get_empty_walk(0, 0))
    # # upper corner spot
    # print(game.get_empty_walk(4, 4))
    # print(game.get_empty_jump(2, 2))
    # print(game.get_empty_jump(2, 3))
    # print(game.get_empty_jump(1, 0))

    # game.set_board_size()
    # game.init_board()
    # game.show_board()

    # x, y = 0, 4
    # x2, y2 = 0, 2
    # print(game.picking_the_piece_legal(x, y))
    # print(game.determine_move_type(x, y, x2, y2))

    # print(game.get_possible_move())
    # print(game.count_total_score())
    # print(game.get_last_move())








    # AI = AI.AI(game, player=((args.player + 1) % 2), max_depth=args.depth)
    # while not game.is_game_complete():
    #     if args.player == 0:
    #         print(args.player)
    #         print("AI 11111111111")
    #         AI.dumb_ai_move(args.player)
    #         args.player = (args.player + 1) % 2
    #
    #     else:
    #         print(args.player)
    #         print("AI 22222222222222")
    #         AI.dumb_ai_move(args.player)
    #         args.player = (args.player + 1) % 2
    #
    #     print(game.is_game_complete(), "*#########################################################***")
    #
    #     print(args.player)
    #     # game.tuen = (game.turn + 1) % 2
    #     print("***************************")






    print("Game over.\nBoard:")
    game.show_board()
    print("\nPlayer 0:", game.count_total_score()[0], "\nPlayer 1:", game.count_total_score()[1],)
    # #
    #
    #
    # game.copy_move([0, 4, 0, 2])

