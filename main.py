from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

from widget import Ui_Form
from game import Game

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        # Grid Layout
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setObjectName("gridLayout")

        # Stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setObjectName("stackedWidget")

        # Menu Page
        self.menuPage = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuPage.sizePolicy().hasHeightForWidth())
        self.menuPage.setSizePolicy(sizePolicy)
        self.menuPage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuPage.setObjectName("menuPage")

        # Menu page main layout
        self.horizontalLayout_menuPage = QtWidgets.QHBoxLayout(self.menuPage)
        self.horizontalLayout_menuPage.setContentsMargins(40,0,40,0)
        self.horizontalLayout_menuPage.setObjectName("horizontalLayout_menuPage")

        # Menu page vertical layout
        self.verticalLayout_menuPage = QtWidgets.QVBoxLayout()
        self.verticalLayout_menuPage.setObjectName("verticalLayout_menuPage")

        # Menu title horizontal layout
        self.horizontalLayout_menuTitle = QtWidgets.QHBoxLayout()
        self.horizontalLayout_menuTitle.setObjectName("horizontalLayout_menuTitle")

        # Left menu title spacer
        spacerItem_titleLeft = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_menuTitle.addItem(spacerItem_titleLeft)

        # Menu title label
        self.label = QtWidgets.QLabel(self.menuPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(96)
        self.label.setFont(font)
        self.label.setObjectName("labelMenu")
        self.horizontalLayout_menuTitle.addWidget(self.label)

        # Right menu title spacer
        spacerItem_titleRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        self.horizontalLayout_menuTitle.addItem(spacerItem_titleRight)

        # Add menu tilte layout to menu page layout
        self.verticalLayout_menuPage.addLayout(self.horizontalLayout_menuTitle)

        # Buttons horizontal layout
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")

        # Buttons left spacer
        spacerItem_buttonsLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        self.horizontalLayout_buttons.addItem(spacerItem_buttonsLeft)

        # Buttons vertical layout
        self.verticalLayout_buttons = QtWidgets.QVBoxLayout()
        self.verticalLayout_buttons.setObjectName("verticalLayout_buttons")
        self.verticalLayout_buttons.setContentsMargins(0,20,0,20)

        # Spacer on game button
        spacerItem3 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem3)

        # Game button 
        self.pushButton_game = QtWidgets.QPushButton(self.menuPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_game.sizePolicy().hasHeightForWidth())
        self.pushButton_game.setSizePolicy(sizePolicy)
        self.pushButton_game.setMinimumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.pushButton_game.setFont(font)
        self.pushButton_game.setObjectName("pushButton_game")
        self.verticalLayout_buttons.addWidget(self.pushButton_game)

        # Spacer under game button
        spacerItem_game = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem_game)

        # Settings Button
        self.pushButtonSettings = QtWidgets.QPushButton(self.menuPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSettings.sizePolicy().hasHeightForWidth())
        self.pushButtonSettings.setSizePolicy(sizePolicy)
        self.pushButtonSettings.setMinimumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.pushButtonSettings.setFont(font)
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.verticalLayout_buttons.addWidget(self.pushButtonSettings)

        # Spacer under settings button
        spacerItem_settings = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem_settings)

        # Exit button
        self.pushButton_exit = QtWidgets.QPushButton(self.menuPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy)
        self.pushButton_exit.setMinimumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.verticalLayout_buttons.addWidget(self.pushButton_exit)

        # Spacer under exit button
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem6)
        
        # Add buttons vertical layout to buttons horizontal layout
        self.horizontalLayout_buttons.addLayout(self.verticalLayout_buttons)

        # Buttons right spacer
        spacerItem7 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_buttons.addItem(spacerItem7)

        # Add buttons horizontal layout to menu page vertical layout
        self.verticalLayout_menuPage.addLayout(self.horizontalLayout_buttons)

        # Add menu page vertical layout to menu page horizontal layout
        self.horizontalLayout_menuPage.addLayout(self.verticalLayout_menuPage)

        # Add menu page to stacked widget
        self.stackedWidget.addWidget(self.menuPage)

        # Add stacked widget to grid layout   
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        # Set central widget in main window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Application exit
        self.pushButton_exit.clicked.connect(QtCore.QCoreApplication.quit)
        
        # End Game
        def endGame(stackedWidget, game):
            stackedWidget.setCurrentIndex(0)
            stackedWidget.removeWidget(stackedWidget.widget(1))
            game.deleteLater()

        # Create game window and set it in stacked widget
        def startGame(stackedWidget):
            game = Game()
            stackedWidget.addWidget(game)
            stackedWidget.setCurrentIndex(1)
            game.endGameSignal.connect(lambda : endGame(stackedWidget, game))

        # Connect StartGame with pushButton_game
        self.pushButton_game.clicked.connect(lambda: startGame(self.stackedWidget))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pawns Game"))
        self.label.setText(_translate("MainWindow", "Pawns Game"))
        self.pushButton_game.setText(_translate("MainWindow", "Graj"))
        self.pushButtonSettings.setText(_translate("MainWindow", "Ustawienia"))
        self.pushButton_exit.setText(_translate("MainWindow", "Wyjście"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())