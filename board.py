#!/usr/bin/env python
import chess
from transposition_table import TranspositionTable

from evaluate import Evaluator


class Board():
    def __init__(self, board=None, tree=None):
        # Make a new board.
        if board:
            self.board = board
        else:
            self.board = chess.Board()

        self.evaluator = Evaluator()

    # Computer move.
    def comp_move(self, depth, evaluator="negamax"):
        if not self.board.is_game_over():
            # Negamax with alpha beta pruning, transposition table and iterative deepening.
            final_move, value, b = self.evaluator.negamax(
                self.board, depth, float("-inf"), float("inf"), None, evaluator)

            move = final_move[-1]

            print("Computer's Move: " + str(move))
            return move
