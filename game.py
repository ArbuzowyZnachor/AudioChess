import logging
import chess
import chess.engine
import chess.svg
import speech
import random
from playsound import playsound

from time import sleep
from threading import Event, Thread
from PodSixNet.Connection import connection, ConnectionListener

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QPushButton

class ChessboardWidget(QSvgWidget):
    repaint_signal = pyqtSignal()
    def __init__(self):
        super().__init__(parent=None)
        self.repaint_signal.connect(lambda: self.repaint())

    def showEvent(self, event):
        self.setFixedWidth(self.height())
    def resizeEvent(self, event):
        self.setFixedWidth(self.height())


class Game(QWidget, ConnectionListener):
    end_game = pyqtSignal()
    threads_stop = False
    engine = None
    gameActive = False
    connected = False

    def __init__(self, online):
        super().__init__(parent=None)
        self.online = online

        self.settings = QSettings('MyQtApp', 'App1')
        self.setFocusPolicy(Qt.StrongFocus)
        
        if(self.online):
            self.player_colour = 2
            self.player_turn = False
        else:
            # Create Stockfish levels
            self.stockfish_level = ((1, 0.05), (2, 0.1), (3, 0.15), 
            (4, 0.2), (6, 0.25), (8, 0.3), (10, 0.35), (12, 0.4))

            # Set singleplayer color and turn
            if(self.settings.value("piecesColor") == "white"):
                self.player_colour = 1
            elif(self.settings.value("piecesColor") == "black"):
                self.player_colour = 0
            else:
                self.player_colour = random.getrandbits(1)
            self.player_turn = bool(self.player_colour)

            # Initialize enigne from exe file
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(
                    "stockfish_20011801_x64.exe")
            except Exception:
                logging.exception('Engine initialization error')
                speech.sayWords("Błąd połączenia z silnikiem szachowym")
                self.end_game.emit()
            
        # Build Game widget layout
        self.gridLayout_main = QHBoxLayout(self)
        self.gridLayout_main.setContentsMargins(0,0,0,0)
        self.wallpaper = QWidget()
        self.wallpaper_layout = QGridLayout(self.wallpaper)
        self.wallpaper_layout.setContentsMargins(0,0,0,0)
        self.gridLayout_main.addWidget(self.wallpaper)
        self.wallpaper.setStyleSheet(".QWidget{\n"
            "border-image: url(:/Images/background.JPG) \
            0 0 0 0 stretch stretch;\n"
            "background-position: center;\n"
            "background-repeat: none\n"
            "}")
        self.widgetSvg = ChessboardWidget()
        self.widgetSvg.setStyleSheet("background-color:white")
        if(self.online):
            self.returnButton = QPushButton("Powrót")
            self.returnButton.setStyleSheet("max-width: 400px;")
            self.returnButton.clicked.connect(lambda: self.end_game.emit())
            self.returnButton.setDisabled(True)
            self.wallpaper_layout.addWidget(self.returnButton)
        else:
            self.wallpaper_layout.addWidget(self.widgetSvg)

        # Initialize chessboard object
        self.chessboard = chess.Board()
        self.print_board()

        # Set threads and events
        self.wellcome_sound_thread = Thread(
            target=self.welcome_sound, name = "Welcome")
        self.wellcome_sound_thread.daemon = True
        if(self.online):
            self.client_thread = Thread(target=self.client, name = "Client")
            self.client_thread.daemon = True
            self.Connect(("localhost", 5554))
            self.client_thread.start()
        else:
            self.engine_move_thread = Thread(
                target=self.engine_move, name = "Engine")
            self.engine_move_thread.daemon = True
            self.engine_move_event = Event()
            self.engine_move_thread.start()
            self.wellcome_sound_thread.start()

#======================== User interface functions ===========================

    # Print chessboard image
    def print_board(self):
        if(self.chessboard.move_stack):
            if(self.chessboard.is_check()):
                self.chessboardSvg = chess.svg.board(
                    self.chessboard,flipped=not self.player_colour, 
                lastmove=self.chessboard.peek(), 
                check=self.chessboard.king(
                    self.chessboard.turn)).encode("UTF-8")
            else:
                self.chessboardSvg = chess.svg.board(self.chessboard,
                flipped=not self.player_colour, 
                lastmove=self.chessboard.peek()).encode("UTF-8")
        else:
            self.chessboardSvg = chess.svg.board(
                self.chessboard,flipped=not self.player_colour
                ).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        self.widgetSvg.repaint_signal.emit()
    
    # Play initial game info (Used in wellcome_sound_thread)
    def welcome_sound(self):
        if(self.settings.value("firstGame", "true") == "true"):
                self.page_sound_text = "Witaj w grze. Aby wykonać ruch \
                    naciśnij spacje i podaj ruch w notacji SAN.\
                    Aby się poddać podaj komendę poddaj się.\
                    Aby sprawdzić zawartość pola na szachownicy,\
                    podaj komendę pole, a następnie nazwę pola na przykład b7"
                speech.sayWords(self.page_sound_text)
                self.settings.setValue("firstGame", "false")
        if(not self.player_turn):
            speech.sayWords("Grę zaczyna przeciwnik")
            self.engine_move_event.set()
        else:
            speech.sayWords("Rozpoczynasz grę")

    # Get and perform player's voice command 
    def player_action(self):
        try:
            data = speech.get_player_action()
            if(data):
                if(data["action"]=="surrender"):
                    speech.sayWords("Koniec gry")
                    self.end_game.emit()
                elif(data["action"]=="checkField"):
                    self.check_field(data["field"])
                elif(data["action"]=="move"):
                    self.player_move(data["move"])
                elif(data["action"] == "error"):
                    playsound("sound/error.mp3")
        except Exception:
            logging.exception("{0} function error:".format(
                self.player_action.__name__))

#======================== Game functions =====================================

    # Check chessboard field content
    def check_field(self, field):
        if(field != "badfield"):
            try:
                piece = self.chessboard.piece_at(
                    chess.SQUARE_NAMES.index(field))
                if(piece):
                    speech.sayPiece(field , piece.color, piece.piece_type)
                else:
                    speech.sayWords("puste")
            except Exception:
                logging.exception("{0} function error:".format(
                    self.check_field.__name__))
        else:
            speech.sayWords("Niepoprawna nazwa pola")

    # Validate and make player move
    def player_move(self, move):
        try:
            move_san = self.chessboard.parse_san(move)
            if(move_san):
                if(self.online):
                    self.send_move(self.chessboard.san(move_san))
                    self.push_move(move_san)
                    self.game_continue()
                else:
                    self.push_move(move_san)
                    if self.game_continue():
                        self.engine_move_event.set()
        except ValueError as ex:
            speech.sayWords("Nieprawidłowy ruch")
        except Exception:
            logging.exception("{0} function error:".format(
                self.player_move.__name__))
        else:
            self.player_turn = False

    # Push move to chessboard object and play sound
    def push_move(self, move):
        try:
            if self.chessboard.is_capture(move):
                self.chessboard.push(move)
                playsound("sound/Capture.mp3")
            else:
                self.chessboard.push(move)
                playsound("sound/Move.mp3")
        except Exception:
            logging.exception("{0} function error:".format(
                self.push_move.__name__))
        else:
            self.print_board()

    # Check game status
    def game_continue(self):
        try:
            if(self.chessboard.is_game_over(claim_draw=False)):
                self.connected = False
                if(self.chessboard.is_variant_draw()):
                    speech.sayWords("Remis")
                elif(self.chessboard.is_checkmate()):
                    speech.sayWords("Mat")
                    if self.player_turn: 
                        speech.sayWords("Wygrywasz")
                    else:
                        speech.sayWords("Przeciwnik wygrywa")
                sleep(2)
                self.end_game.emit()
                return False
            else:
                if(self.chessboard.is_check()):
                    speech.sayWords("Szach")
                return True
        except Exception:
            logging.exception("{0} function error:".format(
                self.game_continue.__name__))

#======================== Singeplayer functions ==============================

    # Generate and push engine move (Used in engine_move_thread)
    def engine_move(self):
        while True:
            self.engine_move_event.wait()
            if(self.threads_stop):
                break
            sleep(1)
            try:
                result = self.engine.play(self.chessboard, 
                chess.engine.Limit(
                    depth = self.stockfish_level
                    [self.settings.value("stockfishLevel") - 1][0], 
                    time = self.stockfish_level
                    [self.settings.value("stockfishLevel") - 1][1]))
                if result:
                    text = self.chessboard.san(result.move)
                    if text:
                        speech.sayMove(text)
                        self.push_move(result.move)
            except Exception:
                logging.exception("{0} function error:".format(
                    self.engine_move.__name__))
                speech.sayWords("Błąd silnika szachowego")
                self.end_game.emit()
            else:
                self.engine_move_event.clear()
                if self.game_continue():
                    self.player_turn = True

#======================== Multiplayer functions ==============================

    # Get player action before started game
    def wait_action(self):
        try:
            data = speech.get_wait_action()
            if(data):
                if(data["action"]=="return"):
                    self.end_game.emit()
        except Exception:
            logging.exception("{0} function error:".format(
                self.wait_action.__name__))

    # Validate and push enemy move
    def enemy_move(self, move_san):
        try:
            move = self.chessboard.parse_san(move_san)
            if move:
                speech.sayMove(move_san)
                self.push_move(move)
        except Exception:
            logging.exception("{0} function error, move = {1}".format(
                self.wait_action.__name_, move_san))
            speech.sayWords("Błąd ruchu przeciwnika")
            self.end_game.emit()
        else:
            if self.game_continue():
                self.player_turn = True

#======================== Game server communication functions ================

    def Network_connected(self, data):
        self.connected = True
        self.returnButton.setDisabled(False)

    def Network_disconnected(self, data):
        speech.sayWords("Błąd połączenia z serwerem")
        self.end_game.emit()

    def Network_error(self, data):
        logging.error("{0} function:".format(
            self.wait_action.__name__))
        connection.Close()

    def Network_setGame(self, data):
        self.returnButton.setDisabled(True)
        if(data["colour"] == "white"):
            self.player_colour = 0
        else:
            self.player_colour = 1

        self.player_turn = bool(self.player_colour)
        self.gameActive = True
        speech.sayWords("Znaleziono grę")
        self.wallpaper_layout.removeWidget(self.returnButton)
        self.wallpaper_layout.addWidget(self.widgetSvg)
        self.print_board()

    def Network_moveFromServer(self,data):
        self.enemy_move(data["move"])

    def Network_resignFromServer(self, data):
        speech.sayWords("Przeciwnik poddał się")
        self.end_game.emit()

    def Network_disconnectedFromServer(self, data):
        logging.error('Game server error: {0}'.format(data["error"]))
        speech.sayWords("Błąd serwera")
        self.end_game.emit()

    def send_move(self, move):
        connection.Send({"action":"move", "move":move})

    def send_resign(self):
        connection.Send({"action":"resign"}) 

    def send_disconnect(self):
        connection.Send({"action":"disconnect"})

    def client(self):
        while True:
            if(self.threads_stop):
                break
            self.Loop()
            sleep(0.001)

    def Loop(self):
        try:
            connection.Pump()
            self.Pump()
        except Exception:
            logging.exception("Loop function error:")
            self.end_game.emit()

#======================== Event and thread functions =========================

    # Key press event slot
    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if(self.online):
                if self.connected:
                    self.player_action()
            elif self.player_turn:
                self.player_action()

    # Delete threads 
    def delete_threads(self):
        if(self.online):
            if(self.connected):
                if(self.gameActive ):
                    self.send_resign()
                else:
                    self.send_disconnect()
                sleep(1)
            self.threads_stop = True
        else:
            self.threads_stop = True
            self.engine.close()
            self.engine_move_event.set()