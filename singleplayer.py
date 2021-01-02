import chess
import chess.engine
import chess.svg
import sys
import recognize_speech as rs
import random
from playsound import playsound

from time import sleep
from threading import Event, Thread

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QGridLayout

class Singleplayer(QWidget):
    end_singleplayer_signal = pyqtSignal()
    threads_stop = False
    ryba = None
    stockfish_level = ((1,0.05), (2, 0.1), (3, 0.15), (4,0.2), (6,0.25), (8, 0.3), (10, 0.35), (12, 0.4))
    def __init__(self):
        super().__init__(parent=None)

        self.settings = QSettings('MyQtApp', 'App1')

        self.setFocusPolicy(Qt.StrongFocus)
        
        # Player colour and turn
        if(self.settings.value("piecesColor") == "white"):
            self.player_colour = 1
        elif(self.settings.value("piecesColor") == "black"):
            self.player_colour = 0
        else:
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
        self.print_board_t = Thread(target=self.print_board)
        self.engineT = Thread(target=self.engine_move)
        self.narratorT = Thread(target=self.welcome_sound)
        self.print_board_t.daemon = True
        self.engineT.daemon = True
        self.print_board_t.name = "Print board"
        self.narratorT.name = "Narrator"
        
        # Preparing events
        self.event_print_board = Event()
        self.event_engine_move = Event()

        # Starting threads
        self.print_board_t.start()
        self.engineT.start()
        
        self.event_print_board.set()
        self.narratorT.start()
        
    # Function for initial game info
    def welcome_sound(self):
        if(self.settings.value("firstGame", "true") == "true"):
                self.page_sound_text = "Witaj w grze. Aby wykonać ruch naciśnij spacje i podaj ruch w notacji SAN.\
                     Aby się poddać podaj komendę poddaj się. Aby sprawdzić zawartość pola na szachownicy,\
                          podaj komendę pole, a następnie a1"
                rs.sayWords(self.page_sound_text)
                self.settings.setValue("firstGame", "false")
        if(not self.player_turn):
            rs.sayWords("Grę zaczyna przeciwnik")
            self.event_engine_move.set()
        else:
            rs.sayWords("Rozpoczynasz grę")

    # Function to refresh chessboard state
    def print_board(self):
        while True:
            if(self.threads_stop):
                print("Print board thread stopped")
                break
            self.event_print_board.wait()
            if(self.chessboard.move_stack):
                if(self.chessboard.is_check()):
                    self.chessboardSvg = chess.svg.board(self.chessboard,flipped=not self.player_colour, 
                    lastmove=self.chessboard.peek(), 
                    check=self.chessboard.king(self.chessboard.turn)).encode("UTF-8")
                else:
                    self.chessboardSvg = chess.svg.board(self.chessboard,
                    flipped=not self.player_colour, 
                    lastmove=self.chessboard.peek()).encode("UTF-8")
            else:
                self.chessboardSvg = chess.svg.board(self.chessboard,flipped=not self.player_colour).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            self.widgetSvg.update()
            self.event_print_board.clear()

    # Function for sound of piece move
    def sound_move(self, move):
        if(self.chessboard.is_capture(move)):
            playsound("sound/Capture.mp3")
        else:
            playsound("sound/Move.mp3")

    # Function to get player move
    def player_move(self):
        try:
            data = rs.get_turn()
            if(data):
                if(data["action"]=="surrender"):
                    rs.sayWords("Poddano się")
                    self.end_singleplayer_signal.emit()
                elif(data["action"]=="checkField"):
                    piece = self.chessboard.piece_at(chess.SQUARE_NAMES.index(data["field"]))
                    if(piece):
                        rs.sayPiece(piece.color, piece.piece_type)
                    else:
                        rs.sayWords("puste")
                elif(data["action"]=="move"):
                    try:
                        move = self.chessboard.parse_san(data["move"])
                        if(move):
                            self.sound_move(move)
                            self.chessboard.push(move)
                            self.event_print_board.set()
                            self.event_engine_move.set()
                            self.player_turn = False
                    except Exception as ex:
                        print("Errror: ", ex)
                        rs.sayWords("Nieprawidłowy ruch")
                elif(data["action"] == "error"):
                    playsound("sound/bad.mp3")
                    print(data["errorMessage"])
        except Exception as ex:
            print("Player move failed. Error: {0}".format(ex))

    # Engine move function
    def engine_move(self):
        while True:
            if(self.threads_stop):
                print("Engine move thread stopped")
                break
            self.event_engine_move.wait()
            sleep(1)
            try:
                result = ryba.play(self.chessboard, chess.engine.Limit( depth = self.stockfish_level[self.settings.value("stockfishLevel") - 1][0], 
                time = self.stockfish_level[self.settings.value("stockfishLevel") - 1][1]))
                if result:
                    # text = result.move.uci() # TODO
                    text = self.chessboard.san(result.move)
                    print(text)
                    if text:
                        rs.sayPcMove(text)
                        self.sound_move(result.move)
                        self.chessboard.push(result.move)
                        self.event_print_board.set()
                        if(self.chessboard.is_checkmate()):
                            rs.sayWords("Mat")
                        elif(self.chessboard.is_check()):
                            rs.sayWords("Szach")
                if(self.chessboard.is_variant_draw()):
                    rs.sayWords("Remis")
                    self.end_singleplayer_signal.emit()
                if(self.chessboard.is_game_over()):
                    rs.sayWords("Przeciwnik wygrywa")
                    self.end_singleplayer_signal.emit()
            except Exception as ex:
                print("Engine move failed. Error: ", ex)
                self.end_singleplayer_signal.emit()
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