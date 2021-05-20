import config
from transposition_table import TranspositionTable
import numpy as np
import chess
import weights


class Evaluator():
    def __init__(self, max_iterations=config.MAX_ITER_MTD, max_search_depth=config.MAX_DEPTH, max_score=config.MAX_SCORE, evaluator="negamax"):
        self.max_iterations = max_iterations
        self.max_search_depth = max_search_depth
        self.max_score = max_score
        self.tt = TranspositionTable()

        self.square_values = {
            # Pawn
            1: np.array([
                0,  0,   0,   0,   0,   0,  0,  0,
                5, 10,  10, -20, -20,  10, 10,  5,
                5, -5, -10,   0,   0, -10, -5,  5,
                0,  0,   0,  20,  20,   0,  0,  0,
                5,  5,  10,  25,  25,  10,  5,  5,
                10, 10,  20,  30,  30,  20, 10, 10,
                50, 50,  50,  50,  50,  50, 50, 50,
                0,  0,   0,   0,   0,   0,  0,  0
            ]),
            # Knight
            2: np.array([
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20,   0,   5,   5,   0, -20, -40,
                -30,   5,  10,  15,  15,  10,   5, -30,
                -30,   0,  15,  20,  20,  15,   0, -30,
                -30,   5,  15,  20,  20,  15,   5, -30,
                -30,   0,  10,  15,  15,  10,   0, -30,
                -40, -20,   0,   0,   0,   0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ]),
            # Bishop
            3: np.array([
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10,   5,  0,    0,   0,   0,   5, -10,
                -10,  10,  10,  10,  10,  10,  10, -10,
                -10,   0,  10,  10,  10,  10,   0, -10,
                -10,   5,  5,   10,  10,   5,   5, -10,
                -10,   0,  5,   10,  10,   5,   0, -10,
                -10,   0,  0,    0,   0,   0,   0, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ]),
            # Rook
            4: np.array([
                0,  0,  0,  5,  5,  0,  0,  0,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                5, 10, 10, 10, 10, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ]),
            # Queen
            5: np.array([
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10,   0,   5,  0,  0,   0,   0, -10,
                -10,   5,   5,  5,  5,   5,   0, -10,
                0,   0,   5,  5,  5,   5,   0,  -5,
                -5,   0,   5,  5,  5,   5,   0,  -5,
                -10,   0,   5,  5,  5,   5,   0, -10,
                -10,   0,   0,  0,  0,   0,   0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ]),
            # King
            6: np.array([
                20,  30,  10,   0,   0,   10, 30,  20,
                20,  20,   0,   0,   0,   0,  20,  20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30
            ]),
            # King End Game
            7: np.array([
                -50, -30, -30, -30, -30, -30, -30, -50,
                -30, -30,  0,    0,   0,   0, -30, -30,
                -30, -10,  20,  30,  30,  20, -10, -30,
                -30, -10,  30,  40,  40,  30, -10, -30,
                -30, -10,  30,  40,  40,  30, -10, -30,
                -30, -10,  20,  30,  30,  20, -10, -30,
                -30, -20, -10,   0,   0, -10, -20, -30,
                -50, -40, -30, -20, -20, -30, -40, -50

            ])
        }

    # Negamax with alpha beta pruning, transposition table, move ordering and iterative deepening.
    def negamax(self, board, depth, alpha, beta, move, evaluator):
        old_alpha = alpha
        # Past moves.
        moves = []
        # Get player number according to the library.
        player = 1 if board.turn else -1
        if depth == 0 or board.is_game_over():
            # entry.score = evaluator(board, entry.result)
            moves.append(move)
            if evaluator == "negamax":
                return moves, self.negamax_evaluate(board) * player, board
            else:
                return moves, self.nn_evaluate(board), board
        # Transposition Table Entry
        ttEntry = self.tt.lookup(board)

        # Transposition Table usage.
        if ttEntry and ttEntry.depth >= depth:
            if ttEntry.flag == 0:
                if not move:
                    move = ttEntry.move
                moves.append(move)
                return moves, ttEntry.value, board
            elif ttEntry.flag == -1:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == 1:
                beta = min(beta, ttEntry.value)

            # alpha-beta cut-off.
            if alpha >= beta:
                if not move:
                    move = ttEntry.move
                moves.append(move)
                return moves, ttEntry.value, board

        value = float("-inf")
        best_move = None
        legal_moves = board.legal_moves

        # For each legal move in the current board state.
        for i in legal_moves:
            # Push the current move to the board.
            board.push(i)

            # Generate new moves and a value (recursive).
            new_moves, current_value, b = self.negamax(
                board, depth - 1, -beta, -alpha, i, evaluator)
            current_value = -current_value

            # Pop so the current displayed board does not change.
            board.pop()

            # Get the maximum value and set best move.
            if current_value > value:
                value = current_value
                moves = new_moves
                best_move = i

            # Redefine alpha.
            alpha = max(alpha, value)

            # alpha-beta cut-off.
            if alpha >= beta:
                break

        # If there is no best move, get current move.
        if not best_move:
            best_move = move

        if value <= old_alpha:
            flag = 1
        elif value >= beta:
            flag = -1
        else:
            flag = 0

        # Store the current board state with other parameters in the transposition table.
        self.tt.store(board, value, flag, depth, best_move)
        moves.append(best_move)
        return moves, value, board

    def _mtd(self, board, depth, firstGuess):
        guess = firstGuess
        finalBoard = None
        upperBound = self.max_score
        lowerBound = -self.max_score
        i = 0

        while lowerBound < upperBound and i < self.max_iterations:
            if guess == lowerBound:
                gamma = guess + 1
            else:
                gamma = guess
            move, guess, finalBoard = self.negamax(
                board, depth, gamma - 1, gamma, None, "neural")
            if guess < gamma:
                upperBound = guess
            else:
                lowerBound = guess
                i = i + 1
        return move, guess, finalBoard

    # MTDf
    def selectMove(self, board):
        guess1 = 1 << 64
        guess2 = 1 << 64
        finalBoard1 = None
        finalBoard2 = None

        for depth in range(2, self.max_search_depth + 1):
            if depth % 2 == 0:
                move, guess1, finalBoard1 = self._mtd(board, depth, guess1)
            else:
                move, guess2, finalBoard2 = self._mtd(board, depth, guess2)

        if self.max_search_depth % 2 == 0:
            return (move, guess1, finalBoard1)
        else:
            return (move, guess2, finalBoard2)

    def clearTranspositionTable(self):
        self.tt = TranspositionTable()

    # Normal Evaluation Function
    def negamax_evaluate(self, board):
        piece_values = {chess.PAWN: 1,
                        chess.KNIGHT: 3,
                        chess.BISHOP: 3,
                        chess.ROOK: 5,
                        chess.QUEEN: 9,
                        chess.KING: 100}

        white_value, black_value = 0, 0
        for p in range(1, 6):
            # Get white pieces.
            white_piece = board.pieces(p, True)
            # Get black pieces.
            black_piece = board.pieces(p, False)
            whites, blacks = 0, 0
            # Get the square value for that piece.
            piece_sq_values = self.square_values[p]
            # Get the piece value.
            piece_value = piece_values[p]*100

            if len(white_piece) > 0:
                # Get the points from the squares with the existing pieces on that square for white.
                whites = piece_sq_values[np.array(list(white_piece))]

            if len(black_piece) > 0:
                # Get the points from the squares with the existing pieces on that square for black.
                blacks = piece_sq_values[-(np.array(list(black_piece)) + 1)]

            # Get white values
            white_value += (np.sum(whites) + len(white_piece) * piece_value)
            # Get black values
            black_value -= (np.sum(blacks) + len(black_piece) * piece_value)

        # Get final value
        final_value = white_value + black_value
        value = final_value / 3500

        # Set the value -1.0, 1.0 or 0.
        value = 1.0 if value > 1.0 else -1.0 if value < -1.0 else value
        return value

    # Neural Network Evaluation Function
    def nn_evaluate(self, board):
        pawnScore = config.PAWN_SCORE
        materialPnts = [pawnScore, 4 * pawnScore,
                        int(round(4.1 * pawnScore)), 6 * pawnScore, 12 * pawnScore, 0]
        phasePoints = [0, 1, 1, 2, 4, 0]
        points = 0

        if board.is_game_over():
            if board.result() == "1-0":
                points = 100
            if board.result() == "1/2-1/2":
                points = 0
            else:
                points = -100
            if not board.turn:
                points = -points
            return points

        materialPoints = initialPoints = endPoints = 0
        phase = totalPhase = 24

        for i in range(0, 64):
            piece = board.piece_at(i)
            if piece:
                phase -= phasePoints[piece.piece_type - 1]
                piece_value = materialPnts[piece.piece_type - 1]
                initial = weights.initPosPnts[piece.piece_type - 1]
                final = weights.finalPosPnts[piece.piece_type - 1]

                if piece.color:
                    materialPoints += piece_value
                    initialPoints += initial[i]
                    endPoints += final[i]
                else:
                    materialPoints -= piece_value
                    initialPoints -= initial[63 - i]
                    endPoints -= final[63 - i]

        phase = (phase * 256 + (totalPhase / 2)) / totalPhase
        points = materialPoints + \
            ((initialPoints * (256 - phase)) + (endPoints * phase)) / 256

        if (board.turn == False):
            points = -points
        return points

    def findFeatures(self, board, color):
        phasePoints = [0, 1, 1, 2, 4, 0]
        featuresRawInit = [[0 for i in range(0, 64)] for j in range(0, 6)]
        featuresRawFin = [[0 for i in range(0, 64)] for j in range(0, 6)]
        featuresInit = []
        featuresFin = []
        colorType = 1 if color else -1
        phase = totalPhase = 24

        for i in range(0, 64):
            piece = board.piece_at(i)
            if piece:
                phase -= phasePoints[piece.piece_type - 1]

        phase = (phase * 256 + (totalPhase / 2)) / totalPhase

        for i in range(0, 64):
            piece = board.piece_at(i)
            if piece:
                initial_features = featuresRawInit[piece.piece_type - 1]
                final_features = featuresRawFin[piece.piece_type - 1]

                if piece.color:
                    initial_features[i] += (256.0 - phase) / 256.0 * colorType
                    final_features[i] += phase / 256.0 * colorType
                else:
                    initial_features[63 -
                                     i] -= (256.0 - phase) / 256.0 * colorType
                    final_features[63 - i] -= phase / 256.0 * colorType

        for j in range(6):
            for i in range(64):
                featuresInit.append(featuresRawInit[j][i])
                featuresFin.append(featuresRawFin[j][i])

        return (featuresInit, featuresFin)
