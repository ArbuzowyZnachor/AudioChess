#! /usr/bin/env python3

import chess
import chess.svg
import sys
import speechRecognize as sr
from stockfish import Stockfish

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        global engine
        engine = Stockfish("D:\Pobrane\stockfish-11-win\stockfish-11-win\Windows\stockfish_20011801_x64.exe")
        super().__init__()
        
        self.setWindowTitle("PawnsGame")
        self.setGeometry(300, 300, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(0, 0, 800, 800)
        
        self.chessboard = chess.Board()

    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            text = sr.getMove()
            if(bool(text)):
                self.chessboard.push_uci(text)
                engine.set_fen_position(self.chessboard.fen())
                self.update()
   
    @pyqtSlot(QWidget)
    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard,flipped=isFlipped).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        


if __name__ == "__main__":
    pawnsGame = QApplication([])
    window = MainWindow()
    window.show()
    pawnsGame.exec()