#! /usr/bin/env python3

import chess
import chess.engine
import chess.svg
import sys
import speechRecognize as sr
import checkboard as check

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

ryba = None

class Game(QWidget):
    endGameSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        global ryba
        ryba = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")
        
        self.setWindowTitle("PawnsGame")
        self.setGeometry(300, 300, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(0, 0, 800, 800)
        
        self.chessboard = chess.Board()

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            text = sr.getMove()
            if(bool(text)):
                if(text=="surrender"):
                    self.endGameSignal.emit()
                else: 
                    move = chess.Move.from_uci(text)
                    if(self.chessboard.is_legal(move)):
                        self.chessboard.push(move)
                        result = ryba.play(self.chessboard, chess.engine.Limit(time=0.1))
                        self.chessboard.push(result.move)
                        check.isGameEnd(self.chessboard)
                        sr.sayMove(result.move.uci())
                    else:
                        print("Illegal move")
                    
   
    @pyqtSlot(QWidget)
    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)