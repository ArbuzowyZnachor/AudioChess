from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QAction

from uifiles.mainUI import Ui_MainWindow

from game import Game

class Ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Ui, self).__init__(parent)
        self.setupUi(self)
        self.showFullScreen()
        self.pushButtonExit.clicked.connect(lambda: self.close())
        self.pushButtonGame.clicked.connect(lambda : self.startGame())
        self.widget_list = []
        self.game = None 

    # End Game
    def endGame(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))
        self.game.deleteThreads()
        self.game.deleteLater()

    # Create game window and set it in stacked widget
    def startGame(self):
        self.game = Game()
        self.widget_list.append(self.game)
        self.stackedWidget.addWidget(self.game)
        self.stackedWidget.setCurrentIndex(1)
        self.game.endGameSignal.connect(lambda : self.endGame())
        
    def closeEvent(self, event):
        print("Exit app")
        if(self.game):
            self.game.deleteThreads()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.show()
    sys.exit(app.exec_())