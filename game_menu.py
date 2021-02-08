
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtWidgets import QWidget
from threading import Event, Thread

from uifiles.gameUI import Ui_gameMenu
import speech

class GameMenu(QWidget, Ui_gameMenu):
    close_game_menu_signal = pyqtSignal()
    start_singleplayer_signal = pyqtSignal()
    start_multiplayer_signal = pyqtSignal()
    block_action_signal = pyqtSignal(object)
    page_communique_signal = pyqtSignal(object)
    
    action_blocked = False
    threads_stop = False

    def __init__(self, parent):
        super(GameMenu, self).__init__(parent)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.pushButtonSingle.clicked.connect(lambda: self.start_singleplayer_signal.emit())
        self.pushButtonExit.clicked.connect(lambda: self.close_game_menu_signal.emit())
        self.pushButtonMulti.clicked.connect(lambda: self.start_multiplayer_signal.emit())
        self.block_action_signal.connect(lambda x:self.block_action(x))

        self.settings = QSettings('UKW', 'AudioChess')

        self.game_menu_command_event = Event()
        self.game_menu_command_thread = Thread(
            target=self.game_menu_command, name="Player action")
        self.game_menu_command_thread.daemon = True
        self.game_menu_command_thread.start()

    def game_menu_command(self):
         while True:
            self.game_menu_command_event.wait()
            if(self.threads_stop):
                break
            try:
                self.block_action_signal.emit(True)
                data = speech.get_game_menu_command()
                if(data):
                    if(data["action"] == "single"):
                        self.start_singleplayer_signal.emit()
                    elif(data["action"] == "multi"):
                        self.start_multiplayer_signal.emit()
                    elif(data["action"] == "exit"):
                        self.close_game_menu_signal.emit()
                    elif(data["action"] == "help"):
                        speech.sayWords(data["helpMessage"])
                    elif(data["action"] == "error"):
                        speech.sayWords(data["errorMessage"])
                    elif(data["action"] == "none"):
                        pass
                    else:
                        speech.sayWords("Brak odpowiedniej opcji")
            except Exception as ex:
                print("Error:", ex)
            self.game_menu_command_event.clear()
            self.block_action_signal.emit(False)

    def block_action(self, bool):
        self.action_blocked = bool
        self.pushButtonSingle.setDisabled(bool)
        self.pushButtonExit.setDisabled(bool)
        self.pushButtonMulti.setDisabled(bool)

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if not self.action_blocked:
                self.game_menu_command_event.set()

    @pyqtSlot(QWidget)
    def showEvent(self,event):
        if(self.settings.value("pageSound") == "true"):
            if(self.settings.value("firstGameMenu", "true") == "true"):
                self.page_sound_text = "Wybór trybu gry. \
                    Dostępne opcje to gra z komputerem, online oraz powrót"
                self.settings.setValue("firstGameMenu", "false")
            else:
                self.page_sound_text = "Wybierz tryb gry"
            self.page_communique_signal.emit(self.page_sound_text)
    
    def delete_threads(self):
        self.threads_stop = True
        self.game_menu_command_event.set()