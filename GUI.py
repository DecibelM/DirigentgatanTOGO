# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime, Qt

class TOGO_UI(QMainWindow):
    #Constructor for TOGO_UI
    def __init__(self,stopList):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.stopList = stopList
        self.setWindowTitle('Travel')
        self.setStyleSheet("background-color: white;")
        self.generalLayout = QGridLayout()
        # Set the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()

    def _createDisplay(self):
        image = QLabel()
        pixmap = QPixmap('Travel_logga.png')
        image.setPixmap(pixmap.scaled(image.size()*0.5, QtCore.Qt.KeepAspectRatio))

        self.generalLayout.addWidget(image, 0, 0, 1, 2)

        label1 = QLabel('<h2>Linje</h2>')
        self.generalLayout.addWidget(label1, 1, 0)

        self.generalLayout.addWidget(QLabel('<h2>Hållplats</h2>'), 1, 1)
        self.generalLayout.addWidget(QLabel('<h2>Mot</h2>'), 1, 2)
        label4 = QLabel('<h2>Om</h2>')
        self.generalLayout.addWidget(label4, 1, 3)

        label4.setStyleSheet("padding-top : 10px;"
                    "padding-left:0px;"
                    "padding-right:5px;"
                    "padding-bottom :10px;")

        self.widgetListName = [None] * 20 * len(self.stopList) # Max 20 entries per stop
        self.widgetListStopTrack = [None] * 20 * len(self.stopList)  # Max 20 entries per stop
        self.widgetListDirection = [None] * 20 * len(self.stopList)  # Max 20 entries per stop
        self.widgetListDeltatime = [None] * 20 * len(self.stopList)  # Max 20 entries per stop

        self.updateButton = QPushButton('Uppdatera')
        self.updateButton.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : white;"
                             "}"
                             )
        self.generalLayout.addWidget(self.updateButton, 0, 3)

        # creating a label object for time and adding it to the display
        self.timelabel = QLabel()
        self.generalLayout.addWidget(self.timelabel,0,2)

    def getQTime(self):
        #Gets current time and sets the time in GUI
        qttime = QTime.currentTime()
        label_time = qttime.toString('hh:mm:ss')
        self.timelabel.setText(label_time)

    def updateView(self, data):
        self.getQTime()
        for j in range(0,len(data)):
            nextEntry=data[j]
            if self.widgetListName[j] is None:
                self.widgetListName[j]=QLabel(nextEntry.name)
                self.generalLayout.addWidget(self.widgetListName[j], j + 2, 0)
                self.widgetListStopTrack[j]=QLabel(nextEntry.stop +", "+nextEntry.track)
                self.generalLayout.addWidget(self.widgetListStopTrack[j], j + 2, 1)
                self.widgetListDirection[j]=QLabel(nextEntry.direction)
                self.generalLayout.addWidget(self.widgetListDirection[j], j + 2, 2)
                self.widgetListDeltatime[j]=QLabel(nextEntry.deltatime + ' min')
                self.generalLayout.addWidget(self.widgetListDeltatime[j], j + 2, 3)
            else:
                self.widgetListName[j].setText(nextEntry.name)
                self.widgetListStopTrack[j].setText(nextEntry.stop + ", " + nextEntry.track)
                self.widgetListDirection[j].setText(nextEntry.direction)
                self.widgetListDeltatime[j].setText(nextEntry.deltatime + ' min')