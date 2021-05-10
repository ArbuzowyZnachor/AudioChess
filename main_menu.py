from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtWidgets import QWidget
from threading import Event, Thread

from graphic.main_menuUI import Ui_mainMenu
import speech
import logging

class MainMenu(QWidget, Ui_mainMenu):
    open_game_menu_signal = pyqtSignal()
    open_settings_menu_signal = pyqtSignal()
    close_signal = pyqtSignal()
    page_communique_signal = pyqtSignal(object)
    block_action_signal = pyqtSignal(object)
    
    action_blocked = False
    threads_stop = False

    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)
        # Setup Ui
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        # Connect signals
        self.pushButtonGame.clicked.connect(
            lambda : self.open_game_menu_signal.emit())
        self.pushButtonSettings.clicked.connect(
            lambda : self.open_settings_menu_signal.emit())
        self.pushButtonExit.clicked.connect(
            lambda: self.close_signal.emit())
        self.block_action_signal.connect(
            lambda x:self.block_action(x))

        # Get application settings
        self.settings = QSettings('UKW', 'AudioChess')

        # Start command thread
        self.main_menu_command_event = Event()
        self.main_menu_command_thread = Thread(
            target = self.main_menu_command, name = "Main menu command")
        self.main_menu_command_thread.daemon = True
        self.main_menu_command_thread.start()

    # Get and perform voice command for main menu page
    def main_menu_command(self):
        while True:
            if(self.threads_stop):
                break
            self.main_menu_command_event.wait()
            try:
                self.block_action_signal.emit(True)
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
            except Exception:
                logging.exception('message')
            self.main_menu_command_event.clear()
            self.block_action_signal.emit(False)

    def block_action(self, bool):
        self.action_blocked = bool
        self.pushButtonExit.setDisabled(bool)
        self.pushButtonGame.setDisabled(bool)
        self.pushButtonSettings.setDisabled(bool)

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if not self.action_blocked:
                self.main_menu_command_event.set()

    @pyqtSlot(QWidget)
    def showEvent(self,event):
        if(self.settings.value("pageSound") == "true"):
            if(self.settings.value("firstMainMenu", "true") == "true"):
                self.page_communique_text = "Witaj w menu głównym gry. \
                    Aby używać komend głosowych naciśnij \
                    przycisk spacji oraz podaj jedną z dostępnych opcji. \
                    Jeżeli potrzebujesz pomocy, podaj komendę pomoc. \
                    Dostępne opcje to rozpocznij gre, \
                        ustawienia oraz wyjscie z programu"
                self.settings.setValue("firstMainMenu", "false")
            else:
                self.page_communique_text = "Menu główne"
            self.page_communique_signal.emit(self.page_communique_text)
    
    def delete_threads(self):
        self.threads_stop = True
        self.main_menu_command_event.set()