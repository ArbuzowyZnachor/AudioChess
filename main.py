import logging
import sys
from game import Game
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtWidgets import QApplication, QWidget

import speech
from threading import Event, Thread

from graphic.mainUI import Ui_MainWindow
from main_menu import MainMenu
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
        self.main_menu = None
        self.game = None
        self.game_menu = None
        self.settings_menu = None

        # Get application settings
        self.settings = QSettings('UKW', 'AudioChess')
        self.settings_init()

        # Setup UI and connect signals
        self.setupUi(self)
        self.setWindowTitle("Audio Szachy")
        self.setWindowIcon(QtGui.QIcon('graphic/icon.png'))
        self.main_menu = MainMenu(self)

        self.block_page_action_signal.connect(
            lambda x: self.block_page_action(x))
        self.main_menu.open_game_menu_signal.connect(
            lambda: self.open_game_menu())
        self.main_menu.open_settings_menu_signal.connect(
            lambda: self.open_settings_menu())
        self.main_menu.close_signal.connect(
            lambda: self.close())
        self.main_menu.page_communique_signal.connect(
            lambda x: self.page_communique(x))

        self.stackedWidget.addWidget(self.main_menu)
        self.stackedWidget.setCurrentIndex(0)
        self.main_menu.setFocus()
        
        # Set pages info sound thread and event
        self.threads_stop = False
        self.say_page_communique_event = Event()
        self.say_page_communique_thread = Thread(
            target=self.say_page_communique, name = "Pages communique")
        self.say_page_communique_thread.daemon = True
        self.say_page_communique_thread.start()

        self.showMaximized()

#======================== Check internet connection ==========================
    def internet_on(self):
        try:
            request.urlopen('http://216.58.192.142', timeout=1)
            return True
        except request.URLError as err: 
            return False

#======================== Set default settings ===============================
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

#======================== App pages functions ================================

    # Open game menu page 
    def open_game_menu(self):
        self.main_menu.clearFocus()
        self.game_menu = GameMenu(self)
        self.stackedWidget.addWidget(self.game_menu)
        self.game_menu.page_communique_signal.connect(
            lambda x: self.page_communique(x))
        self.stackedWidget.setCurrentIndex(1)
        self.game_menu.close_game_menu_signal.connect(
            lambda : self.close_game_menu())
        self.game_menu.start_singleplayer_signal.connect(
            lambda: self.start_game(False))
        self.game_menu.start_multiplayer_signal.connect(
            lambda: self.start_game(True))
        self.game_menu.setFocus()

    # Close game menu page
    def close_game_menu(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.main_menu.setFocus()

    # Open game page
    def start_game(self, online):
        self.game = Game(online)
        self.game.page_communique_signal.connect(
            lambda x: self.page_communique(x))
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

    # Open settings menu page
    def open_settings_menu(self):
        self.main_menu.clearFocus()
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.page_communique_signal.connect(lambda x: self.page_communique(x))
        self.stackedWidget.addWidget(self.settings_menu)
        self.stackedWidget.setCurrentIndex(1)
        self.settings_menu.setFocus()
        self.settings_menu.close_settings_menu_signal.connect(
            lambda: self.close_settings_menu())

    # Close settings menu page
    def close_settings_menu(self):
        self.settings_menu.clearFocus()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.main_menu.setFocus()

#======================== Pages communique functions =========================

    # Say page communique
    def say_page_communique(self):
        while True:
            if(self.threads_stop):
                break
            self.say_page_communique_event.wait()
            self.say_page_communique_event.clear()
            self.block_page_action_signal.emit(True)
            speech.sayWords(self.communique_text)
            self.block_page_action_signal.emit(False)

    # Get page communique text and set event
    def page_communique(self, text):
        self.communique_text = text
        self.say_page_communique_event.set()

    # Block or release current widget actions
    def block_page_action(self, bool):
        self.stackedWidget.currentWidget().block_action(bool)

#======================== Event functions ====================================
    # Delete all leftover threads
    @pyqtSlot(QWidget)
    def closeEvent(self, event):
        if(self.main_menu):
            self.main_menu.delete_threads()
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