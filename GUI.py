# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout

class TOGO_UI(QMainWindow):
    #Constructor for TOGO_UI
    def __init__(self,stopList):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.stopList = stopList
        self.setWindowTitle(self.stopList[0]+' and '+self.stopList[1])
        self.generalLayout = QGridLayout()
        # Set the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()

    def _createDisplay(self):
        self.generalLayout.addWidget(QLabel('<p style="text-align:center;"><h1>TOGO</h1></p>'), 0, 0, 1, 3)

        self.generalLayout.addWidget(QLabel('Linje'), 1, 0)
        self.generalLayout.addWidget(QLabel('Hållplats'), 1, 1)
        self.generalLayout.addWidget(QLabel('Mot'), 1, 2)
        self.generalLayout.addWidget(QLabel('Om'), 1, 3)

        self.widgetListName = [None] * 20 * len(self.stopList) # Max 20 entries per stop
        self.widgetListStopTrack = [None] * 20 * len(self.stopList)  # Max 20 entries per stop
        self.widgetListDirection = [None] * 20 * len(self.stopList)  # Max 20 entries per stop
        self.widgetListDeltatime = [None] * 20 * len(self.stopList)  # Max 20 entries per stop

        self.updateButton = QPushButton('Uppdatera')
        self.generalLayout.addWidget(self.updateButton, 0, 3)

    def updateView(self, data):
        k=0
        for i in range(0,len(self.stopList)):
            for j in range(0,len(data[self.stopList[i]])):
                nextEntry=data[self.stopList[i]][j]
                if self.widgetListName[k+j] is None:
                    print("None",k,j)
                    self.widgetListName[k+j]=QLabel(nextEntry.name)
                    self.generalLayout.addWidget(self.widgetListName[k + j], k + j + 2, 0)
                    self.widgetListStopTrack[k+j]=QLabel(self.stopList[i]+", "+nextEntry.track)
                    self.generalLayout.addWidget(self.widgetListStopTrack[k+j], k + j + 2, 1)
                    self.widgetListDirection[k+j]=QLabel(nextEntry.direction)
                    self.generalLayout.addWidget(self.widgetListDirection[k+j], k + j + 2, 2)
                    self.widgetListDeltatime[k+j]=QLabel(nextEntry.deltatime + ' min')
                    self.generalLayout.addWidget(self.widgetListDeltatime[k+j], k + j + 2, 3)
                else:
                    print("else",k,j)
                    self.widgetListName[k+j].setText(nextEntry.name)
                    self.widgetListStopTrack[k + j].setText(self.stopList[i] + ", " + nextEntry.track)
                    self.widgetListDirection[k + j].setText(nextEntry.direction)
                    self.widgetListDeltatime[k + j].setText(nextEntry.deltatime + ' min')
            k = k+len(data[self.stopList[abs(i)]])