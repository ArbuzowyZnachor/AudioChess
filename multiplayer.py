#! /usr/bin/env python3

import chess
import chess.engine
import chess.svg
import sys
import speechRecognize as sr
import checkboard as check

from time import sleep
import threading

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QGridLayout

from PodSixNet.Connection import ConnectionListener, connection

ryba = None

class Game(QWidget, ConnectionListener):
    endGameSignal = pyqtSignal()

    def __init__(self):
        super().__init__(parent=None)
        
        # global ryba
        # ryba = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")
        self.gridLayout_main = QGridLayout(self)
        self.gridLayout_main.setContentsMargins(0,0,0,0)
        self.setStyleSheet("background: blue")

        self.widgetSvg = QSvgWidget()
        self.gridLayout_main.addWidget(self.widgetSvg)

        # Sets svg widget position in self parent
        self.widgetSvg.setGeometry(0, 0, 800, 800)
        
        self.chessboard = chess.Board()
        self.chessboardSvg = chess.svg.board(self.chessboard,flipped=False).encode("UTF-8") #flipped to rotate board
        self.widgetSvg.load(self.chessboardSvg)

    def printBoard(self):
        self.chessboardSvg = chess.svg.board(self.chessboard,flipped=False).encode("UTF-8") #flipped to rotate board
        self.widgetSvg.load(self.chessboardSvg)
        self.widgetSvg.update()

    def kolejka(self):
        text = sr.getMoveBetter()
        if(bool(text)):
            if(text=="surrender"):
                self.t._delete()
                ryba.quit()
                self.endGameSignal.emit()
            else: 
                move = self.chessboard.parse_san(text)
                if(move):
                    self.chessboard.push(move)
                    self.printBoard()
                    sleep(2)

                    result = ryba.play(self.chessboard, chess.engine.Limit(time=0.1)) #changed to 1 from 0.1
                    self.chessboard.push(result.move)
                    check.isGameEnd(self.chessboard)
                    sr.sayMove(result.move.uci())
                    print(result.move.uci())
                    sleep(2)
                    self.printBoard()
                else:
                    print("Illegal move")

    def watek(self):
        # if self.t.is_alive:
        #     self.t._delete # TODO
        self.t = threading.Thread(target=self.kolejka)
        self.t.start()

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.watek()

    @pyqtSlot(QWidget)
    def resizeEvent(self, event):
        self.widgetSvg.setFixedWidth(self.widgetSvg.height())