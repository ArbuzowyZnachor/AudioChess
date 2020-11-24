#! /usr/bin/env python3

import chess
import chess.engine
import chess.svg
import sys
import speechRecognize as sr
import random

from time import sleep
from threading import Event, Thread

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QGridLayout
from playsound import playsound

ryba = None

class Game(QWidget):
    endGameSignal = pyqtSignal()
    threads_stop = False
    def __init__(self):
        super().__init__(parent=None)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus(True)
        # Player colour and turn
        self.player_colour = random.getrandbits(1)
        self.player_turn = bool(self.player_colour)

        # Enigne initializing from exe file
        global ryba
        ryba = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")

        # Setting layout
        self.gridLayout_main = QGridLayout(self)
        self.gridLayout_main.setContentsMargins(0,0,0,0)
        self.widgetSvg = QSvgWidget()
        self.gridLayout_main.addWidget(self.widgetSvg)

        # Sets svg widget position in self parent
        self.widgetSvg.setGeometry(0, 0, 800, 800)

        # Initializing chessboard
        self.chessboard = chess.Board()

        # Preparing threads
        self.printboardT = Thread(target=self.printBoard)
        self.engineT = Thread(target=self.engine_move)
        self.narratorT = Thread(target=self.narratorStart)
        self.printboardT.daemon = True
        self.engineT.daemon = True
        
        # Preparing events
        self.event_print_board = Event()
        self.event_engine_move = Event()

        # Starting threads
        self.printboardT.start()
        self.engineT.start()
        
        self.event_print_board.set()
        self.narratorT.start()
        
        
    def narratorStart(self):
        if(not self.player_turn):
            sr.sayWords("Grę zaczyna przeciwnik")
            self.event_engine_move.set()
        else:
            sr.sayWords("Rozpoczynasz grę, twoja tura")
        pass


    # Function to refresh chessboard state
    def printBoard(self):
        while True:
            if(self.threads_stop):
                print("Print board thread stopped")
                break
            self.event_print_board.wait()
            if(self.chessboard.move_stack):
                if(self.chessboard.is_check()):
                    self.chessboardSvg = chess.svg.board(self.chessboard,flipped=not self.player_colour, lastmove=self.chessboard.peek(), check=self.chessboard.king(self.chessboard.turn)).encode("UTF-8")
                else:
                    self.chessboardSvg = chess.svg.board(self.chessboard,flipped=not self.player_colour, lastmove=self.chessboard.peek()).encode("UTF-8")
            else:
                self.chessboardSvg = chess.svg.board(self.chessboard,flipped=not self.player_colour).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            self.widgetSvg.update()
            self.event_print_board.clear()

    def soundMove(self, move):
        print(move)
        if(self.chessboard.is_capture(move)):
            playsound("sound/Capture.mp3")
        else:
            playsound("sound/Move.mp3")

    # Function to get player 
    def player_move(self):
        # TODO Space for sound effect
        try:
            text = sr.getMoveBetter()
            if(bool(text)):
                if(text=="surrender"):
                    print("Poddaje sie")
                    self.endGameSignal.emit()
                else: 
                    move = self.chessboard.parse_san(text)
                    if(move):
                        self.soundMove(move)
                        self.chessboard.push(move)
                        self.event_print_board.set()
                    else:
                        print("Illegal move")
                    self.event_engine_move.set()
                    self.player_turn = False
        except Exception as ex:
            print("Player move failed. Error: {0}".format(ex))

    # Engine move function
    def engine_move(self):
        # print("Engine move start function")
        while True:
            if(self.threads_stop):
                print("Engine move thread stopped")
                break
            self.event_engine_move.wait()
            sleep(2)
            try:
                result = ryba.play(self.chessboard, chess.engine.Limit(time=0.1)) #changed to 1 from 0.1
                sr.sayMove(result.move.uci())
                self.soundMove(result.move)
                self.chessboard.push(result.move)
                self.event_print_board.set()
                if(self.chessboard.is_game_over()):
                    sr.sayWords("Przeciwnik wygrywa")
                    self.endGameSignal.emit()
            except Exception as ex:
                print("Engine move failed. Error: ", ex)
                self.endGameSignal.emit()
            else:
                self.player_turn = True
                self.event_engine_move.clear()
            
    # Key press event slot
    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and self.player_turn:
            self.player_move()

    # Resize event slot
    @pyqtSlot(QWidget)
    def resizeEvent(self, event):
        self.widgetSvg.setFixedWidth(self.widgetSvg.height())

    def deleteThreads(self):
        print("Deleting threads")
        ryba.close()
        self.threads_stop = True