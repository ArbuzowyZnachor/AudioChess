import chess
import chess.engine
import chess.svg
import sys
import recognize_speech as rs
import random
from playsound import playsound

from time import sleep
from threading import Event, Thread
from PodSixNet.Connection import connection, ConnectionListener


from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QGridLayout

class Multiplayer(QWidget, ConnectionListener):
    end_multiplayer_signal = pyqtSignal()
    threads_stop = False
    
    def __init__(self):
        super().__init__(parent=None)

        self.settings = QSettings('MyQtApp', 'App1')
        self.player_colour = 2
        self.player_turn = False
        # self.con

        self.setFocusPolicy(Qt.StrongFocus)

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
        self.client_t = Thread(target=self.client)
        self.narratorT = Thread(target=self.welcome_sound)

        self.print_board_t.daemon = True
        self.client_t.daemon = True
        self.print_board_t.name = "Print board"
        self.narratorT.name = "Narrator"
        
        # Preparing events
        self.event_print_board = Event()
        self.event_engine_move = Event()

        # Starting threads
        self.client_t.start()
        
        self.event_print_board.set()
        # self.narratorT.start()
        self.Connect(("localhost", 5555))

    def Loop(self):
        connection.Pump()
        self.Pump()

    # Sends move to server
    def send_move(self, move):
        connection.Send({"action":"move", "move":move})
        print("wysłano ruch")

    def send_resign(self):
        connection.Send({"action":"resign"}) 
        print("wysłano poddanie się")


    def Network_moveFromServer(self,data):
        # print("Ruch przeciwnika: ", data["move"])

        # self.move = data["move"]
        self.engine_move(data["move"])
        print("Odebrano ruch")
        print("Ruch przeciwnika: ", data["move"])

    def Network_resignFromServer(self, data):
        print("oh no my queen")
        rs.sayWords("Przeciwnik poddał się")
        self.end_multiplayer_signal.emit()


    def Network_setGame(self, data):
        # print("Numer twojej gry: {0} Twój kolor: {1}".format(data["gameNumber"], data["colour"]))
        if(data["colour"] == "white"):
            self.player_colour = 0
        else:
            self.player_colour = 1

        self.player_turn = bool(self.player_colour)
        rs.sayWords("Znaleziono grę")
        

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        # print('Utracono połączenie z serwerem')
        # exit()
        rs.sayWords("Błąd połączenia z serwerem")
        self.end_multiplayer_signal.emit()

    def client(self):
        self.print_board_t.start()
        while True:
            if(self.threads_stop):
                print("Game client thread stopped")
                break
            self.Loop()
            sleep(0.001)


    # Function for initial game info
    def welcome_sound(self):
        if(self.settings.value("firstGame", "true") == "true"):
                self.page_sound_text = "Witaj w grze. Aby wykonać ruch naciśnij spacje i podaj ruch w notacji SAN.\
                     Aby się poddać podaj komendę poddaj się. Aby sprawdzić zawartość pola na szachownicy,\
                          podaj komendę pole, a następnie a1"
                rs.sayWords(self.page_sound_text)
                self.settings.setValue("firstGame", "false")
        # if(not self.player_turn):
        #     rs.sayWords("Grę zaczyna przeciwnik")
        #     self.event_engine_move.set()
        # else:
        #     rs.sayWords("Rozpoczynasz grę")

    # Function to refresh chessboard state
    def print_board(self):
        while True:
            if(self.threads_stop):
                print("Print board thread stopped")
                break
            self.event_print_board.wait()
            if self.player_colour != 2:
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
                    print("Poddano się")
                    self.send_resign()
                    self.end_multiplayer_signal.emit()
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
                            move_san = self.chessboard.san(move)
                            self.sound_move(move)
                            self.chessboard.push(move)
                            self.event_print_board.set()
                            self.send_move(move_san)
                            self.event_engine_move.set()
                            self.player_turn = False
                    except Exception as ex:
                        print("Errror: ", ex)
                        rs.sayWords("Nieprawidłowy ruch")
                elif(data["action"] == "error"):
                    print(data["errorMessage"])
        except Exception as ex:
            print("Player move failed. Error: {0}".format(ex))

    # Engine move function
    def engine_move(self, move_san):
        try:
            move = self.chessboard.parse_san(move_san)
            if move:
                rs.sayPcMove(move_san)
                self.sound_move(move)
                self.chessboard.push(move)
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
        self.threads_stop = True