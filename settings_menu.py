from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QAction

from threading import Event, Thread

from uifiles.settingsUI import Ui_Form
import speech

class SettingsMenu(QWidget, Ui_Form):
    close_settings_menu_signal = pyqtSignal()

    def __init__(self, parent):
        super(SettingsMenu, self).__init__(parent)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.settings = QSettings('UKW', 'AudioChess')

        # Set slider value
        self.horizontalSlider_stockfish_lvl.setValue(self.settings.value("stockfishLevel"))

        # Set pieces color radioButtons
        if(self.settings.value("piecesColor") == "white"):
            self.radioButton_white.setChecked(True)
        elif(self.settings.value("piecesColor") == "black"):
            self.radioButton_black.setChecked(True)
        else:
            self.radioButton_random.setChecked(True)

        # Set page info sound radioButtons
        if(self.settings.value("pageSound") == "true"):
            self.radioButton_info_on.setChecked(True)
        else:
            self.radioButton_info_off.setChecked(True)

        # Connect buttond to functions and signals
        self.pushButton_return.clicked.connect(lambda: self.close_settings_menu_signal.emit())
        self.pushButton_save.clicked.connect(lambda: self.save_settings())

        self.helpMessage = "Dostępne opcje to: poziom komputera od jeden do osiem. Kolor figur: białe, czarne albo losowe. \
                    Dźwięk aktywnego mikrofonu: włączony albo wyłączony. Oraz komunikaty głosowe: włączone lub wyłączone. \
                    Zapisz aby zapisać zmiany. Powrót aby wrócić do menu"

    # Function to save settings before exit
    def save_settings(self):
        self.settings.setValue("stockfishLevel", self.horizontalSlider_stockfish_lvl.value())

        if(self.radioButton_white.isChecked()):
            self.settings.setValue("piecesColor", "white")
        elif(self.radioButton_black.isChecked()):
            self.settings.setValue("piecesColor","black")
        else:
            self.settings.setValue("piecesColor", "random")

        if(self.radioButton_info_on.isChecked()):
            self.settings.setValue("pageSound", "true")
        else:
            self.settings.setValue("pageSound", "false")
        pass

    def get_settings_command(self):
        try:
            data = speech.get_settings_action()
            if(data["action"] == "engine"):
                self.horizontalSlider_stockfish_lvl.setValue(int(data["level"]))
                text = "Ustawiono poziom trudności na " + str(data["level"])
                self.horizontalSlider_stockfish_lvl.update()
                speech.sayWords(text)

            elif(data["action"] == "piecesColor"):
                if data["piecesColor"] == "white":
                    self.radioButton_white.setChecked(True)
                    speech.sayWords("Ustawiono kolor figur na biały")
                elif data["piecesColor"] == "black":
                    self.radioButton_black.setChecked(True)
                    speech.sayWords("Ustawiono kolor figur na czarny")
                elif data["piecesColor"] == "random":
                    self.radioButton_random.setChecked(True)
                    speech.sayWords("Ustawiono kolor figur na losowy")
                
            elif(data["action"] == "pageSound"):
                if data["pageSound"] == "on":
                    self.radioButton_info_on.setChecked(True)
                    speech.sayWords("Włączono komunikaty głosowe")
                elif data["pageSound"] == "off":
                    self.radioButton_info_off.setChecked(True)
                    speech.sayWords("Wyłączono komunikaty głosowe")

            elif(data["action"] == "help"):
                speech.sayWords(self.helpMessage)

            elif(data["action"] == "return"):
                self.close_settings_menu_signal.emit()

            elif(data["action"] == "save"):
                self.save_settings()
                speech.sayWords("Zapisano ustawienia")

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
            self.get_settings_command()