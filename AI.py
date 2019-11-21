#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible", "https://github.com/cheind/py-classic-ai/blob/master/connectfour.py"]
__version__ = "0.0.3"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


from sys import float_info
import Game_play

print(float_info.max)


class AI:
    '''Artificial agent playing connect-four.'''

    def __init__(self, max_depth=4, y=0.9):
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
        self.board = Game_play.GamePlay().board
        self.max_depth = max_depth
        self.player = Game_play.GamePlay().turn
        self.y = 0.9

    # def minimax(self, position, depth, alphabeta, maximizing_player):
    #     if depth == 0 or game == over in position:
    #         return static evaluation of position
    #
    #     if maximizing_player:
    #         maxEval = -infinity
    #         for child in position:
    #             eval = minimax(child, depth - 1, alpha, beta, False)
    #             maxEval = max(maxEval, eval)
    #             alpha = max(alpha, eval)
    #             if beta <= alpha:
    #                 break
    #             return maxEval
    #
    #     else:
    #         minEval = +infinity
    #         for child in position:
    #             eval = minimax (child, depth - 1, alpha, beta, True)
    #             minEval = min(minEval, eval)
    #             beta = min(beta, eval)
    #             if beta <= alpha:
    #                 break
    #         return minEval

# initial call
# minimax(currentPosition, 3, -INFINITY, INFINITY, true)

    def move(self):
        '''Take the move that optimizes this players outcome.'''
        best = self.negamax(self.Gameplay, -float_info.max, float_info.max, 0, self.player)
        print("best",best)
        self.Gameplay.make_move(best[1][0], best[1][1], best[1][2], best[1][3])

    def negamax(self, Gameplay, alpha, beta, depth, player):
        '''Recursively optimize the moves assuming the opponent plays optimal.'''
        if self.terminal(Gameplay, depth):
            return self.utility(Gameplay, player)
        else:
            v = (-float_info.max, None)
            for m in Gameplay.get_possible_move():
                score, move = self.negamax(Gameplay.copy_move(m), -beta, -alpha, depth + 1, 1 - player)
                score *= -1 * self.y ** depth

                if score > v[0]:
                    v = (score, m)

                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return v

    def terminal(self, Gameplay, depth):
        '''Test if current state is terminal.'''
        return depth == self.max_depth or Gameplay.is_game_complete()

    def utility(self, Gameplay, player):
        '''Returns the utility score for the given player.'''
        return (Gameplay.count_total_score()[player], Gameplay.get_last_move)


# if __name__ == '__main__':
#     AI = AI()
#     print(AI.Gameplay.board)
