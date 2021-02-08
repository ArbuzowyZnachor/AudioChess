import logging
import sys
import pyttsx3
from game import Game
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QSettings
from PyQt5.QtWidgets import QApplication, QWidget

import speech
from threading import Event, Thread

from uifiles.mainUI import Ui_MainWindow
from game import Game
from game_menu import GameMenu
from settings_menu import SettingsMenu

from urllib import request

logging.basicConfig(filename='client_errors.log', level=logging.ERROR)

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    open_game_menu_signal = pyqtSignal()
    open_settings_menu_signal = pyqtSignal()
    close_signal = pyqtSignal()
    block_page_action_signal = pyqtSignal(object)

    action_blocked = False

    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        if(not self.internet_on()):
            speech.sayWords("Brak połączenia z siecią, wyjście z programu")
            sys.exit()
        
        # Setup pages objects
        self.game = None
        self.game_menu = None
        self.settings_menu = None

        # Setup signals
        self.open_game_menu_signal.connect(lambda: self.open_game_menu())
        self.open_settings_menu_signal.connect(lambda: self.open_settings_menu())
        self.close_signal.connect(lambda: self.close())
        self.block_page_action_signal.connect(lambda x: self.block_page_action(x))

        # Get application settings
        self.settings = QSettings('UKW', 'AudioChess')
        # self.settings.clear()
        self.settings_init()

        # Setup UI and connect buttons to functions
        self.setupUi(self)
        self.setWindowTitle("Audio Szachy")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.pushButtonExit.clicked.connect(lambda: self.close())
        self.pushButtonGame.clicked.connect(lambda : self.open_game_menu())
        self.pushButtonSettings.clicked.connect(lambda : self.open_settings_menu())

        # Set pages info sound thread and event
        self.threads_stop = False
        self.say_page_communique_event = Event()
        self.say_page_communique_thread = Thread(target=self.say_page_communique, name = "Pages communique")
        self.say_page_communique_thread.daemon = True
        self.say_page_communique_thread.start()

        self.main_menu_command_event = Event()
        self.main_menu_command_thread = Thread(
            target = self.main_menu_command, name = "Main menu command")
        self.main_menu_command_thread.daemon = True
        self.main_menu_command_thread.start()
        # self.showMaximized() # TODO DEBUG

    # Settings init 
    def settings_init(self):
        if(self.settings.value("firstStart", "true") == "true"):
            self.settings.setValue("firstStart", "false")
            self.settings.setValue("stockfishLevel", 4)
            self.settings.setValue("piecesColor", "random")
            self.settings.setValue("pageSound", "true")
            self.settings.setValue("firstMainMenu", "true")
            self.settings.setValue("firstGameMenu", "true")
            self.settings.setValue("firstSettingsMenu", "true")
            self.settings.setValue("firstGame", "true")

    # Internet connection check
    def internet_on(self):
        try:
            request.urlopen('http://216.58.192.142', timeout=1)
            return True
        except request.URLError as err: 
            return False

#======================== Voice command function =============================

    # Get and perform voice command for main menu
    def main_menu_command(self):
        while True:
            if(self.threads_stop):
                break
            self.main_menu_command_event.wait()
            try:
                self.block_action(True)
                data = speech.get_main_menu_command()
                if(data):
                    if(data["action"] == "play"):
                        self.open_game_menu_signal.emit()
                    elif(data["action"] == "settings"):
                        self.open_settings_menu_signal.emit()
                    elif(data["action"] == "exit"):
                        self.close_signal.emit()
                    elif(data["action"] == "help"):
                        speech.sayWords(data["helpMessage"])
                    elif(data["action"] == "error"):
                        speech.sayWords(data["errorMessage"])
                    elif(data["action"] == "none"):
                        pass
                    else:
                        speech.sayWords("Brak odpowiedniej opcji")                                     
            except Exception as ex:
                logging.exception('message')
            self.main_menu_command_event.clear()
            self.block_action(False)

#======================== App pages functions ================================

    # Open game menu page 
    def open_game_menu(self):
        self.menuPage.clearFocus()
        self.game_menu = GameMenu(self)
        self.stackedWidget.addWidget(self.game_menu)
        self.game_menu.page_communique_signal.connect(lambda x: self.page_communique(x))
        self.stackedWidget.setCurrentIndex(1)
        self.game_menu.close_game_menu_signal.connect(
            lambda : self.close_game_menu())
        self.game_menu.start_singleplayer_signal.connect(
            lambda: self.start_game(False))
        self.game_menu.start_multiplayer_signal.connect(
            lambda: self.start_game(True))
        self.game_menu.setFocus()
        # self.game_menu_sound()
        

    # Close game menu page
    def close_game_menu(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.menuPage.setFocus()
        self.main_menu_sound()

    # Open game page
    def start_game(self, online):
        self.game = Game(online)
        self.stackedWidget.addWidget(self.game)
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.widget(1).clearFocus()
        self.game.end_game_signal.connect(lambda : self.end_game())
        self.game.setFocus()

    # Close game page
    def end_game(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.widget(2).clearFocus()
        self.stackedWidget.removeWidget(self.stackedWidget.widget(2))
        self.stackedWidget.widget(1).setFocus()
        self.game.delete_threads()
        self.game.deleteLater()
        self.game_menu_sound()

    # Open settings menu page
    def open_settings_menu(self):
        self.menuPage.clearFocus()
        self.settings_menu = SettingsMenu(self)
        self.stackedWidget.addWidget(self.settings_menu)
        self.stackedWidget.setCurrentIndex(1)
        self.settings_menu.setFocus()
        self.settings_menu.close_settings_menu_signal.connect(
            lambda: self.close_settings_menu())
        self.settings_menu_sound()

    # Close settings menu page
    def close_settings_menu(self):
        self.settings_menu.clearFocus()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.menuPage.setFocus()
        self.main_menu_sound()


#======================== Pages communique functions =========================

    # Pages sound (Used in page_sound_thread)
    def say_page_communique(self):
        while True:
            if(self.threads_stop):
                break
            self.say_page_communique_event.wait()
            self.say_page_communique_event.clear()
            self.block_page_action_signal.emit(True)
            speech.sayWords(self.page_communique_text)
            self.block_page_action_signal.emit(False)

    def page_communique(self, text):
        self.page_communique_text = text
        self.say_page_communique_event.set()

    def block_page_action(self, bool):
        self.stackedWidget.currentWidget().block_action(bool)

    def block_action(self, bool):
        self.action_blocked = bool
        self.pushButtonExit.setDisabled(bool)
        self.pushButtonGame.setDisabled(bool)
        self.pushButtonSettings.setDisabled(bool)

    # Play main menu communique sound
    def main_menu_sound(self):
        if(self.settings.value("pageSound") == "true"):
            if(self.settings.value("firstMainMenu", "true") == "true"):
                self.page_communique_text = "Witaj w menu głównym gry. \
                    Aby używać komend głosowych naciśnij \
                    przycisk spacji oraz podaj jedną z dostępnych opcji. \
                    Jeżeli potrzebujesz pomocy, podaj komendę pomoc. \
                    Dostępne opcje to rozpocznij gre, \
                        ustawienia oraz wyjscie z programu"
                self.say_page_communique_event.set()
                self.settings.setValue("firstMainMenu", "false")
            else:
                self.page_communique_text = "Menu główne"
                self.say_page_communique_event.set()
        pass
    # Play setting menu communique sound
    def settings_menu_sound(self):
        # if(self.settings.value("pageSound") == "true"):
        #     self.page_sound_text = "Ustawienia"
        #     self.page_sound_event.set()
        #     if(self.settings.value("firstSettingsMenu", "true") == "true"):
        #         self.page_sound_text = "\
        #             Dostępne opcje to: poziom komputera od jeden do osiem. \
        #             Kolor figur: białe, czarne albo losowe. \
        #             Dźwięk aktywnego mikrofonu: włączony albo wyłączony. \
        #             Oraz komunikaty głosowe: włączone lub wyłączone. \
        #             Zapisz aby zapisać zmiany. Powrót aby wrócić do menu"
        #         self.page_sound_event.set()
        #         self.settings.setValue("firstSettingsMenu", "false")
        pass

    # Play game menu communique sound
    def game_menu_sound(self):
        # if(self.settings.value("pageSound") == "true"):
        #     if(self.settings.value("firstGameMenu", "true") == "true"):
        #         self.page_sound_text = "Wybór trybu gry. \
        #             Dostępne opcje to gra z komputerem, online oraz powrót"
        #         self.page_sound_event.set()
        #         self.settings.setValue("firstGameMenu", "false")
        #     else:
        #         self.page_sound_text = "Wybierz tryb gry"
        #         self.page_sound_event.set()
        pass

#======================== Event functions ====================================

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if not self.action_blocked:
                self.main_menu_command_event.set()

    @pyqtSlot(QWidget)
    def showEvent(self, event):
        self.main_menu_sound()

    @pyqtSlot(QWidget)
    def closeEvent(self, event):
        if(self.game):
            self.game.delete_threads()
        if(self.game_menu):
            self.game_menu.delete_threads()
        if(self.settings_menu):
            self.settings_menu.delete_threads()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())