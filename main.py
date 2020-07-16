#! /usr/bin/env python3

import chess
import chess.engine
import chess.svg
import sys
import speechRecognize as sr

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

ryba = None

class MainWindow(QWidget):
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
                move = chess.Move.from_uci(text)
                if(self.chessboard.is_legal(move)):
                    self.chessboard.push(move)
                    self.update()
                    result = ryba.play(self.chessboard, chess.engine.Limit(time=0.1))
                    # sr.sayMove(result.move.uci())
                    # print(" ".join(result.move.uci()))
                    self.chessboard.push(result.move) 
                else:
                    print("Illegal move")
   
    @pyqtSlot(QWidget)
    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == "__main__":
    pawnsGame = QApplication([])
    window = MainWindow()    
    window.show()
    pawnsGame.exec()