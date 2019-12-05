#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible", "https://github.com/cheind/py-classic-ai/blob/master/connectfour.py",
               "https://www.youtube.com/watch?v=l-hh51ncgDI"]
__version__ = "0.0.3"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


from sys import float_info
import Game_play

print(float_info.max)


class AI:
    '''Artificial agent playing connect-four.'''

    def __init__(self, board, player=None, max_depth=4, y=0.9):
        '''Initialize agent.
        Params
        ------
        board : Board
            Board to play
        player : int
            Which player to take on (0 or 1)
        Kwargs
        ------
        max_depth : int
            Since exhaustive planning takes exponential time,
            this value limits the look-ahead capability of the agent.
        y : float
            Discount factor for future events
        '''

        self.Gameplay = Game_play.GamePlay()

        if board is None:
            self.board = Game_play.GamePlay().board
        else:
            self.board = board
            # self.Gameplay.board = board
        self.max_depth = max_depth
        if player is None:
            self.player = Game_play.GamePlay().turn
        else:
            self.player = player
        self.y = 0.9
        self.last_move = None

    # Psudo code from https://www.youtube.com/watch?v=l-hh51ncgDI
    #     def minimax(self, position, depth, alphabeta, maximizing_player):
    #         if depth == 0 or game == over in position:
    #             return static evaluation of position
    #
    #         if maximizing_player:
    #             maxEval = -infinity
    #             for child in position:
    #                 eval = minimax(child, depth - 1, alpha, beta, False)
    #                 maxEval = max(maxEval, eval)
    #                 alpha = max(alpha, eval)
    #                 if beta <= alpha:
    #                     break
    #                 return maxEval
    #
    #         else:
    #             minEval = +infinity
    #             for child in position:
    #                 eval = minimax (child, depth - 1, alpha, beta, True)
    #                 minEval = min(minEval, eval)
    #                 beta = min(beta, eval)
    #                 if beta <= alpha:
    #                     break
    #             return minEval
    #
    # initial call
    # minimax(currentPosition, 3, -INFINITY, INFINITY, true)

    def dumb_ai_move(self, player=None):
        best = self.dumb(self.Gameplay, 1, True, self.player)
        print('dumb_ai_move', best[1][0], best[1][1], best[1][2], best[1][3], self.player)
        self.Gameplay.make_move(best[1][0], best[1][1], best[1][2], best[1][3], self.player)

    def dumb(self, Gameplay, depth, maximizing_player, turn):
        # if self.terminal(Gameplay, depth):
        if depth == 0 or self.Gameplay.is_game_complete():
            return self.Gameplay.count_total_score(Gameplay.board), self.last_move

        if maximizing_player:
            max_eval = -float_info.max
            for move in Gameplay.get_possible_move(turn):
                eval = self.dumb(Gameplay.copy_move(move), depth - 1, False, turn)
                if eval[0] > max_eval:
                    max_eval = eval
                    self.last_move = move
                # max_eval = max(max_eval, eval)
            return max_eval, move

        else:
            min_eval = float_info.max
            print("////////////////////////////////////////////////////////////////////\n\n\n\n\n\n",
                  Gameplay.get_possible_move((turn + 1)% 2),
                  '\n\n\n\n\n\n\n\n\n')
            for move in Gameplay.get_possible_move((turn + 1)% 2):
                eval = self.dumb(move, depth - 1, False, turn)
                if eval[0] < min_eval:
                    min_eval = eval
                    self.last_move = move
                min_eval = min(min_eval, eval)
            return min_eval, move

    def move(self, player=None):
        '''Take the move that optimizes this players outcome.'''
        best = self.negamax(self.Gameplay, -float_info.max, float_info.max, 0, self.player)
        print("best", best)
        self.Gameplay.make_move(best[1][0], best[1][1], best[1][2], best[1][3], self.player)

    def negamax(self, Gameplay, alpha, beta, depth, player):
        '''Recursively optimize the moves assuming the opponent plays optimal.'''
        if self.terminal(Gameplay, depth):
            return self.utility(Gameplay, player)
        else:
            if player:
                # Gameplay = Game_play.GamePlay(board=self.board.board)

                v = (-float_info.max, None)
                Gameplay.board
                # if self.last_move is None:
                #     moves_to_try = Gameplay.get_possible_move(player)
                # else:
                #     test = self.board.board
                #     game = Game_play.GamePlay(board=self.board.board).get_possible_move(player, self.board.board)
                #     moves_to_try = Game_play.GamePlay(board=self.board.board).get_possible_move(player, self.board.board)
                #     # moves_to_try = Game_play.GamePlay(board=self.board, turn=self.turn, score=self.score).get_possible_move(player)

                moves_to_try = Gameplay.get_possible_move(player, Gameplay.board)

                for m in moves_to_try:
                    self.last_move = m

                    score, move = self.negamax(Gameplay.copy_move(m), -beta, -alpha, depth + 1, (player+1)%2)
                    score *= -1 * self.y ** depth
                    print("score", score, 'player', player, "depth", depth)
                    if score > v[0]:
                        v = (score, m)  # move

                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                    test2 = Gameplay.board
                return v
            else:
                v = (-float_info.max, None)
                for m in Gameplay.get_possible_move(player):
                    score, move = self.negamax(Gameplay.copy_move(m), -beta, -alpha, depth + 1, (player + 1) % 2)
                    # self.last_move = m
                    score *= -1 * self.y ** depth
                    print("score", score, 'player', player, "depth", depth)
                    if score < v[0]:
                        v = (score, m)  # move

                    beta = min(beta, score)
                    if beta <= alpha:
                        break
                return v


    def terminal(self, Gameplay, depth):
        '''Test if current state is terminal.'''
        return depth == self.max_depth or Gameplay.is_game_complete()

    def utility(self, Gameplay, player):
        '''Returns the utility score for the given player.'''
        print(Gameplay.get_last_move())
        print(self.last_move)
        return (Gameplay.count_total_score()[player], Gameplay.get_last_move())


# if __name__ == '__main__':
#     AI = AI()
#     print(AI.Gameplay.board)
