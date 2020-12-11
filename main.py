from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QAction

import recognize_speech as rs
from threading import Event, Thread

from uifiles.mainUI import Ui_MainWindow
from singleplayer import Singleplayer
from game_menu import GameMenu
from settings_menu import SettingsMenu

class Ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Ui, self).__init__(parent)
        # Get application settings
        self.settings = QSettings('MyQtApp', 'App1')
        # self.settings.clear() # DEBUG
        self.settings_init()

        # Set pages info sound thread and event
        self.event_page_sound = Event()
        self.threads_stop = False
        self.page_sound_thread = Thread(target=self.page_sound)
        self.page_sound_thread.daemon = True
        self.page_sound_thread.start()
        # self.main_menu_sound()

        # Setup UI and connect buttons to functions
        self.setupUi(self)
        # self.showFullScreen() # TODO DEBUG
        self.pushButtonExit.clicked.connect(lambda: self.close())
        self.pushButtonGame.clicked.connect(lambda : self.open_game_menu())
        self.pushButtonSettings.clicked.connect(lambda : self.open_settings_menu())

        # Setup class logic
        self.singleplayer = None
        self.multiplayer = None

    # Settings init 
    def settings_init(self):
        if(self.settings.value("firstStart", "true") == "true"):
            self.settings.setValue("firstStart", "false")
            self.settings.setValue("stockfishLevel", 4)
            self.settings.setValue("piecesColor", "random")
            self.settings.setValue("activeMicSound", "true")
            self.settings.setValue("pageSound", "true")
            self.settings.setValue("firstMainMenu", "true")
            self.settings.setValue("firstGameMenu", "true")
            self.settings.setValue("firstSettingsMenu", "true")
            self.settings.setValue("firstGame", "true")

    # Pages sound (Used in pages sound thread)
    def page_sound(self):
        while True:
            if(self.threads_stop):
                break
            self.event_page_sound.wait()
            self.event_page_sound.clear()
            rs.sayWords(self.page_sound_text)

    # Create and display game menu window 
    def open_game_menu(self):
        self.menuPage.clearFocus()
        self.game_menu = GameMenu(self)
        self.stackedWidget.addWidget(self.game_menu)
        self.stackedWidget.setCurrentIndex(1)
        self.game_menu.close_game_menu_signal.connect(lambda : self.close_game_menu())
        self.game_menu.start_singleplayer_signal.connect(lambda: self.start_singleplayer())
        self.game_menu.setFocus()

    # Return from game menu
    def close_game_menu(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.menuPage.setFocus()

    # Starts game with computer
    def start_singleplayer(self):
        self.singleplayer = Singleplayer()
        self.stackedWidget.addWidget(self.singleplayer)
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.widget(1).clearFocus()
        self.singleplayer.end_singleplayer_signal.connect(lambda : self.end_singleplayer())
        self.singleplayer.setFocus()

    # Closes game with computer
    def end_singleplayer(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.widget(2).clearFocus
        self.stackedWidget.removeWidget(self.stackedWidget.widget(2))
        self.stackedWidget.widget(1).setFocus()
        self.singleplayer.deleteThreads()
        self.singleplayer.deleteLater()

    def open_settings_menu(self):
        self.menuPage.clearFocus()
        self.settings_menu = SettingsMenu(self)
        self.stackedWidget.addWidget(self.settings_menu)
        self.stackedWidget.setCurrentIndex(1)
        self.settings_menu.setFocus()
        self.settings_menu.close_settings_menu_signal.connect(lambda: self.close_settings_menu())

    def close_settings_menu(self):
        self.settings_menu.clearFocus()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.menuPage.setFocus()

    # Get voice command for main menu action
    def main_menu_command(self):
        try:
            data = rs.get_main_menu_action()
            if(data):
                if(data["action"] == "play"):
                    self.open_game_menu()
                elif(data["action"] == "settings"):
                    self.open_settings_menu()
                elif(data["action"] == "exit"):
                    self.close()
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

    def main_menu_sound(self):
        if(self.settings.value("pageSound") == "true"):
            if(self.settings.value("firstMainMenu", "true") == "true"):
                self.page_sound_text = "Witaj w menu głównym gry. Aby używać komend głosowych naciśnij \
                    przycisk spacji oraz podaj jedną z dostępnych opcji. \
                    Jeżeli potrzebujesz pomocy, podaj komendę pomoc. \
                    Dostępne opcje to rozpocznij gre, ustawienia oraz wyjscie z programu"
                self.event_page_sound.set()
                self.settings.setValue("firstMainMenu", "false")
            else:
                self.page_sound_text = "Menu główne"
                self.event_page_sound.set()
    
    def settings_menu_sound(self):
        if(self.settings.value("pageSound") == "true"):
            self.page_sound_text = "Ustawienia"
            self.event_page_sound.set()
            if(self.settings.value("firstSettingsMenu", "true") == "true"):
                self.page_sound_text = "Dostępne opcje to: poziom komputera od jeden do osiem. Kolor figur: białe, czarne albo losowe. \
                    Dźwięk aktywnego mikrofonu: włączony albo wyłączony. Oraz komunikaty głosowe: włączone lub wyłączone. \
                    Zapisz aby zapisać zmiany. Powrót aby wrócić do menu"
                self.event_page_sound.set()
                self.settings.setValue("firstSettingsMenu", "false")

    def game_menu_sound(self):
        if(self.settings.value("pageSound") == "true"):
            if(self.settings.value("firstGameMenu", "true") == "true"):
                self.page_sound_text = "Wybór trybu gry. Dostępne opcje to gra z komputerem, online oraz powrót"
                self.event_page_sound.set()
                self.settings.setValue("firstGameMenu", "false")
            else:
                self.page_sound_text = "Wybierz tryb gry"
                self.event_page_sound.set()

    @pyqtSlot(QWidget)
    def closeEvent(self, event):
        self.settings.setValue
        if(self.singleplayer):
            self.singleplayer.deleteThreads()

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.main_menu_command()

    @pyqtSlot(QWidget)
    def showEvent(self, event):
        self.main_menu_sound()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.show()
    sys.exit(app.exec_())