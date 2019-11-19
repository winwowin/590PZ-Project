#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible", "https://www.redblobgames.com/grids/hexagons/"]
__version__ = "0.1.0"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


import tkinter as tk


class GamePlay(object):

    def __init__(self, board_size=7, num_player=2):
        self.EDGE_SIZE = board_size  # move horizontal
        self.history = []
        self.board = [[-1 for y in range(self.EDGE_SIZE)] for x in range(self.EDGE_SIZE)]
        self.turn = 0
        self.game_complete = 0
        self.num_player = num_player

    def show_board(self):
        print(self.board)

    def init_board(self):
        self.board[0][0] = 1
        self.board[self.EDGE_SIZE -1][self.EDGE_SIZE -1] = 1
        self.board[self.EDGE_SIZE -1][0] = 0
        self.board[0][self.EDGE_SIZE -1] = 0

    # def set_board_size(self):
    #     GamePlay.__init__.EDGE_SIZE = int(input("Set up board size of ?x?: "))
    #     GamePlay.__init__.board = [[-1 for y in range(self.EDGE_SIZE)] for x in range(self.EDGE_SIZE)]

    def is_game_complete(self) -> bool:
        for j in self.board:
            for i in j:
                if i == -1:
                    return False
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


    def get_empty_around(self, x, y):
        """Same with above but contain both 3x3 and 5x5 space. AKA all legal move"""
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
        elif (x2, y2) in self.get_empty_walk(x, y):
            return 'jump'

    def is_move_syntactic(self) -> bool:
        pass

    def is_location_valid(self) -> bool:
        ''' Doe not applied since it's on click, which is always valid. '''
        return True

    def get_game_state(self):
        return self.turn

    # def init_game(self, size: int):
    #     pass

    '''
    hold for later

    def decide_move():
        pass
    '''

    def get_history(self, n: int):
        return self.history

    def make_history(self, x, y):
        self.history.append([self.current_turn, x, y])
        return self.history

    def update_state_with_move(self, move):
        pass

    def determine_next_player(self):
        if GamePlay().turn == 1:
            return "yellow"
        elif GamePlay().turn == 0:
            return "blue"

    # def num_player(self):
    #     pass

    # def current_lo(self):
    #     pass

    def current_turn(self):
        # if self.turn == 0:
        #     return '0'
        # else:
        #     return '1'
        return self.turn

    def whose_turn(self):
        if GamePlay().turn == 1:
            return "blue"
        else:
            return "yellow"

    def make_move(self, x, y, x2, y2):
        if self.picking_the_piece_legal(x, y):
            if self.moving_the_piece_legal(x, y, x2, y2):
                if self.determine_move_type(x, y, x2, y2) == 'walk':
                    self.board[y2][x2] = self.board[y][x]
                elif self.determine_move_type(x, y, x2, y2) == 'jump':
                    self.board[y2][x2] = self.board[y][x]
                    self.board[y][x] = -1


if __name__ == '__main__':
    game = GamePlay(5)
    game.init_board()
    game.show_board()
    print(game.is_game_complete())
    print(game.is_empty_spot(2, 3))

    # # Finding legal move spots
    # # middle spot
    # print(game.get_empty_walk(2, 3))
    # # lower corner spot
    # print(game.get_empty_walk(0, 0))
    # # upper corner spot
    # print(game.get_empty_walk(4, 4))
    print(game.get_empty_jump(2, 2))
    # print(game.get_empty_jump(2, 3))
    # print(game.get_empty_jump(1, 0))

    # game.set_board_size()
    # game.init_board()
    # game.show_board()

