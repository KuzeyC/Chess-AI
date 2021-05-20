#!/usr/bin/env python
import random
import chess
from entry import Entry
import sys


class TranspositionTable:
    def __init__(self):
        # Generate hashes only once.
        self.keys = self.gen_zobrist_keys()
        # Create table only once.
        self.table = {}

    def store(self, state, value, flag, depth, move):
        # Hash the current state and save it in the transposition table.
        # Key: Hash
        # Value: Table Entry Object
        self.table[self.zobrist_hash(state)] = Entry(
            value, flag, depth, move)

    # Search if that hash exists in the transposition table.
    def lookup(self, state):
        return self.table.get(self.zobrist_hash(state))

    # Generate Transposition Table with hashes.
    def gen_zobrist_keys(self):
        keys = {}
        # For each square.
        for i in range(64):
            row = {}
            # For each piece symbol.
            for j in "rnbkqpPQKBNR":
                # Random integer between 0 and maximum int.
                # Key: Symbol
                # Value: Random int
                row[j] = random.randint(0, sys.maxsize)
            # Save it to the table
            # Key: Square index
            # Value: Dictionary of hashed pieces
            keys[i] = row
        # Return the transposition table.
        return keys

    def zobrist_hash(self, state):
        # Get the pieces on the board.
        piece_map = state.piece_map()
        h = 0
        # For each piece.
        for i in piece_map:
            # Get the symbol.
            symbol = piece_map[i].symbol()
            # xor current hash with that hash of that piece on that square.
            h ^= self.keys[i][symbol]
        # Return final hash.
        return h
