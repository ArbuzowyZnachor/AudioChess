#! /usr/bin/env python3
from chess import Board

def isGameEnd(board):
    if(board.is_checkmate()):
        print("Checkmate!")
        board.clear_board()

