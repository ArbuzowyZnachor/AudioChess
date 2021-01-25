from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QAction

from uifiles.gameUI import Ui_gameMenu
import speech

class GameMenu(QWidget, Ui_gameMenu):
    close_game_menu_signal = pyqtSignal()
    start_singleplayer_signal = pyqtSignal()
    start_multiplayer_signal = pyqtSignal()
    def __init__(self, parent):
        super(GameMenu, self).__init__(parent)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.pushButtonSingle.clicked.connect(lambda: self.start_singleplayer_signal.emit())
        self.pushButtonExit.clicked.connect(lambda: self.close_game_menu_signal.emit())
        self.pushButtonMulti.clicked.connect(lambda: self.start_multiplayer_signal.emit())

    def game_menu_action(self):
        try:
            data = speech.get_game_menu_action()
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

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.game_menu_action()