import chess
import chess.engine
import chess.svg
import speech
from playsound import playsound

from time import sleep
from threading import Event, Thread, active_count
from PodSixNet.Connection import connection, ConnectionListener

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

class ChessboardWidget(QSvgWidget):
    def showEvent(self, event):
        self.setFixedWidth(self.height())
    def resizeEvent(self, event):
        self.setFixedWidth(self.height())

class Multiplayer(QWidget, ConnectionListener):
    end_multiplayer_signal = pyqtSignal()
    threads_stop = False
    gameActive = False
    
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
        self.wallpaper = QWidget()
        self.wallpaper_layout = QGridLayout(self.wallpaper)
        self.wallpaper_layout.setContentsMargins(0,0,0,0)
        self.gridLayout_main.addWidget(self.wallpaper)
        self.widgetSvg = ChessboardWidget()
        self.widgetSvg.setStyleSheet("background-color:white")
        self.wallpaper.setStyleSheet(".QWidget{\n"
            "border-image: url(:/Images/background.JPG) 0 0 0 0 stretch stretch;\n"
            "background-position: center;\n"
            "background-repeat: none;\n"
            "}\n"
            "}")

        self.returnButton = QPushButton("Powrót")
        self.returnButton.setStyleSheet("max-width: 400px;")
        self.returnButton.clicked.connect(lambda: self.send_disconnect())
        self.wallpaper_layout.addWidget(self.returnButton)

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
        self.event_enemy_move = Event()

        # Starting threads
        self.client_t.start()
        
        self.event_print_board.set()
        # self.narratorT.start()
        self.Connect(("localhost", 5554))

    def Loop(self):
        connection.Pump()
        self.Pump()

    # Sends move to server
    def send_move(self, move):
        connection.Send({"action":"move", "move":move})

    def send_resign(self):
        connection.Send({"action":"resign"}) 
        print("resign")

    def send_disconnect(self):
        connection.Send({"action":"disconnect"})
        print("dissconnect")

    def Network_moveFromServer(self,data):
        self.enemy_move(data["move"])

    def Network_resignFromServer(self, data):
        speech.sayWords("Przeciwnik poddał się")
        self.end_multiplayer_signal.emit()

    def Network_setGame(self, data):
        if(data["colour"] == "white"):
            self.player_colour = 0
        else:
            self.player_colour = 1

        self.player_turn = bool(self.player_colour)
        self.gameActive = True
        speech.sayWords("Znaleziono grę")
        self.wallpaper_layout.removeWidget(self.returnButton)
        self.wallpaper_layout.addWidget(self.widgetSvg)
        self.widgetSvg.setFixedWidth(self.widgetSvg.height())

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        speech.sayWords("Błąd połączenia z serwerem")
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
                speech.sayWords(self.page_sound_text)
                self.settings.setValue("firstGame", "false")
        if(not self.player_turn):
            speech.sayWords("Grę zaczyna przeciwnik")
            self.event_enemy_move.set()
        else:
            speech.sayWords("Rozpoczynasz grę")

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
                sleep(1)
                self.widgetSvg.setFixedWidth(self.widgetSvg.height())
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
            data = speech.get_turn()
            if(data):
                if(data["action"]=="surrender"):
                    print("Poddano się")
                    self.send_resign()
                    self.end_multiplayer_signal.emit()
                elif(data["action"]=="checkField"):
                    piece = self.chessboard.piece_at(chess.SQUARE_NAMES.index(data["field"]))
                    if(piece):
                        speech.sayPiece(piece.color, piece.piece_type)
                    else:
                        speech.sayWords("puste")
                elif(data["action"]=="move"):
                    try:
                        move = self.chessboard.parse_san(data["move"])
                        if(move):
                            move_san = self.chessboard.san(move)
                            self.sound_move(move)
                            self.chessboard.push(move)
                            self.event_print_board.set()
                            self.send_move(move_san)
                            self.event_enemy_move.set()
                            self.player_turn = False
                    except Exception as ex:
                        print("Errror: ", ex)
                        speech.sayWords("Nieprawidłowy ruch")
                elif(data["action"] == "error"):
                    print(data["errorMessage"])
        except Exception as ex:
            print("Player move failed. Error: {0}".format(ex))

    # Engine move function
    def enemy_move(self, move_san):
        try:
            move = self.chessboard.parse_san(move_san)
            if move:
                speech.sayPcMove(move_san)
                self.sound_move(move)
                self.chessboard.push(move)
                self.event_print_board.set()
                if(self.chessboard.is_checkmate()):
                    speech.sayWords("Mat")
                elif(self.chessboard.is_check()):
                    speech.sayWords("Szach")
                    
                if(self.chessboard.is_variant_draw()):
                    speech.sayWords("Remis")
                    self.end_singleplayer_signal.emit()
                if(self.chessboard.is_game_over()):
                    speech.sayWords("Przeciwnik wygrywa")
                    self.endGameSignal.emit()

        except Exception as ex:
            print("Engine move failed. Error: ", ex)
            self.endGameSignal.emit()
        else:
            self.player_turn = True
            self.event_enemy_move.clear()
            
    # Key press event slot
    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and self.player_turn:
            self.player_move()

    def deleteThreads(self):
        print("Deleting threads")
        if(self.gameActive):
            self.send_resign()
        else:
            self.send_disconnect()
        sleep(1)
        self.threads_stop = True