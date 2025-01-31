from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QSettings
from PyQt5.QtWidgets import QWidget

from threading import Event, Thread

from graphic.settingsUI import Ui_Form
import speech

class SettingsMenu(QWidget, Ui_Form):
    close_settings_menu_signal = pyqtSignal()
    set_engine_lvl_signal = pyqtSignal(object)
    set_pieces_color_signal = pyqtSignal(object)
    set_pages_sound_signal = pyqtSignal(object)
    save_settings_signal = pyqtSignal()
    block_action_signal = pyqtSignal(object)
    page_communique_signal = pyqtSignal(object)
    threads_stop = False
    action_blocked = False

    def __init__(self, parent):
        super(SettingsMenu, self).__init__(parent)
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.settings = QSettings('UKW', 'AudioChess')

        self.set_engine_lvl_signal.connect(lambda x: self.set_engine_lvl(x))
        self.set_pieces_color_signal.connect(lambda x: self.set_pieces_color(x))
        self.set_pages_sound_signal.connect(lambda x: self.set_pages_sound(x))
        self.save_settings_signal.connect(lambda: self.save_settings())
        self.block_action_signal.connect(lambda x:self.block_action(x))
        
        self.pushButton_return.clicked.connect(
            lambda: self.close_settings_menu_signal.emit())
        self.pushButton_save.clicked.connect(lambda: self.save_settings())

        # Set slider value
        self.horizontalSlider_stockfish_lvl.setValue(
            self.settings.value("stockfishLevel"))

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

        self.helpMessage = "Dostępne opcje to: poziom komputera od jeden do osiem. \
            Kolor figur: białe, czarne albo losowe. \
            Komunikaty głosowe: włączone lub wyłączone. \
            Aby zapisać zmiany wybierz: Zapisz. \
            Aby wrócić do menu głównego wybierz: Powrót"

        self.settings_command_event = Event()
        self.settings_command_thread = Thread(
            target=self.settings_command, name = "Settings command")
        self.settings_command_thread.daemon = True
        self.settings_command_thread.start()

    def settings_command(self):
         while True:
            self.settings_command_event.wait()
            if(self.threads_stop):
                break
            try:
                self.block_action_signal.emit(True)
                data = speech.get_settings_command()
                if(data["action"] == "engine"):
                    self.set_engine_lvl_signal.emit(data["level"])

                elif(data["action"] == "piecesColor"):
                    self.set_pieces_color_signal.emit(data["piecesColor"])
                    
                elif(data["action"] == "pageSound"):
                    self.set_pages_sound_signal.emit(data["pageSound"])

                elif(data["action"] == "help"):
                    self.page_communique_signal.emit(self.helpMessage)

                elif(data["action"] == "return"):
                    self.close_settings_menu_signal.emit()

                elif(data["action"] == "save"):
                    self.save_settings()
                    self.page_communique_signal.emit("Zapisano ustawienia")

                elif(data["action"] == "error"):
                    self.page_communique_signal.emit(data["errorMessage"])

                elif(data["action"] == "none"):
                    pass
                else:
                    self.page_communique_signal.emit("Brak odpowiedniej opcji")                                     
            except Exception as ex:
                print("Error:", ex)
            self.settings_command_event.clear()
            self.block_action_signal.emit(False)
    
    def set_engine_lvl(self, lvl):
        self.horizontalSlider_stockfish_lvl.setValue(int(lvl))
        text = "Ustawiono poziom trudności na " + str(lvl)
        self.horizontalSlider_stockfish_lvl.update()
        self.page_communique_signal.emit(text)   

    def set_pieces_color(self, color):
        if color == "white":
            self.radioButton_white.setChecked(True)
            self.page_communique_signal.emit("Ustawiono kolor figur na biały")
        elif color == "black":
            self.radioButton_black.setChecked(True)
            self.page_communique_signal.emit("Ustawiono kolor figur na czarny")
        elif color == "random":
            self.radioButton_random.setChecked(True)
            self.page_communique_signal.emit("Ustawiono kolor figur na losowy")

    def set_pages_sound(self, sound):
        if sound == "on":
            self.radioButton_info_on.setChecked(True)
            self.page_communique_signal.emit("Włączono komunikaty głosowe")
        elif sound == "off":
            self.radioButton_info_off.setChecked(True)
            self.page_communique_signal.emit("Wyłączono komunikaty głosowe")

    # Save settings before exit settings page
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

    def block_action(self, bool):
        self.action_blocked = bool

        self.radioButton_info_on.setDisabled(bool)
        self.radioButton_info_off.setDisabled(bool)

        self.radioButton_black.setDisabled(bool)
        self.radioButton_white.setDisabled(bool)
        self.radioButton_random.setDisabled(bool)

        self.horizontalSlider_stockfish_lvl.setDisabled(bool)
        self.pushButton_return.setDisabled(bool)
        self.pushButton_save.setDisabled(bool)

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.settings_command_event.set()

    @pyqtSlot(QWidget)
    def showEvent(self,event):
        if(self.settings.value("pageSound") == "true"):
            self.page_communique_text = "Ustawienia"
            if(self.settings.value("firstSettingsMenu", "true") == "true"):
                self.page_communique_text = "\
                    Dostępne opcje to: poziom komputera od jeden do osiem. \
                    Kolor figur: białe, czarne albo losowe. \
                    Dźwięk aktywnego mikrofonu: włączony albo wyłączony. \
                    Oraz komunikaty głosowe: włączone lub wyłączone. \
                    Zapisz aby zapisać zmiany. Powrót aby wrócić do menu"
                self.settings.setValue("firstSettingsMenu", "false")
            self.page_communique_signal.emit(self.page_communique_text)

    def delete_threads(self):
        self.threads_stop = True
        self.settings_command_event.set()