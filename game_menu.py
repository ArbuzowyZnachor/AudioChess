from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QAction

from uifiles.gameUI import Ui_Form
import recognize_speech as rs

class GameMenu(QWidget, Ui_Form):
    close_game_menu_signal = pyqtSignal()
    start_singleplayer_signal = pyqtSignal()
    def __init__(self, parent):
        super(GameMenu, self).__init__(parent)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.pushButtonSingle.clicked.connect(lambda: self.start_singleplayer_signal.emit())
        self.pushButtonExit.clicked.connect(lambda: self.close_game_menu_signal.emit())

    def game_menu_action(self):
        try:
            data = rs.get_game_menu_action()
            if(data):
                if(data["action"] == "single"):
                    self.start_singleplayer_signal.emit()
                elif(data["action"] == "multi"):
                    pass
                elif(data["action"] == "exit"):
                    self.close_game_menu_signal.emit()
                elif(data["action"] == "help"):
                    rs.sayWords(data["helpMessage"])
                elif(data["action"] == "error"):
                    rs.sayWords(data["errorMessage"])
                elif(data["action"] == "none"):
                    pass
                else:
                    rs.sayWords("Brak odpowiedniej opcji")
        except Exception as ex:
            print("Error:", ex)

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.game_menu_action()