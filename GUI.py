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
        # main does not exist once this is called
        self.generalLayout.addWidget(QLabel('<p style="text-align:center;"><h1>TOGO</h1></p>'), 0, 0, 1, 3)
        self.generalLayout.addWidget(QLabel(self.stopList[0]), 1, 0)

        self.generalLayout.addWidget(QLabel('Avgång'), 2, 0)
        self.generalLayout.addWidget(QLabel('Mot'), 2, 1)
        self.generalLayout.addWidget(QLabel('Tid'), 2, 2)
        self.vagn1 = QLabel('Transportmedel')
        self.generalLayout.addWidget(self.vagn1, 3, 0)
        self.mot1 = QLabel('Slutdestination')
        self.generalLayout.addWidget(self.mot1, 3, 1)
        self.time1 = QLabel('Datum och tid')
        self.generalLayout.addWidget(self.time1, 3, 2)

        self.generalLayout.addWidget(QLabel(self.stopList[1]), 4, 0)

        self.generalLayout.addWidget(QLabel('Avgång'), 5, 0)
        self.generalLayout.addWidget(QLabel('Mot'), 5, 1)
        self.generalLayout.addWidget(QLabel('Tid'), 5, 2)
        self.vagn2 = QLabel('Transportmedel')
        self.generalLayout.addWidget(self.vagn2, 6, 0)
        self.mot2 = QLabel('Slutdestination')
        self.generalLayout.addWidget(self.mot2, 6, 1)
        self.time2 = QLabel('Datum och tid')
        self.generalLayout.addWidget(self.time2, 6, 2)

        self.updateButton = QPushButton('Uppdatera')
        self.generalLayout.addWidget(self.updateButton, 7, 1)

        #self.tableWidget = QTableWidget()
        #self.generalLayout.addWidget(self.tableWidget, 8, 0, 1, 3)


    def updateView(self, data):
        nextDeparture = data[self.stopList[0]][0]
        self.vagn1.setText(nextDeparture.name)
        self.time1.setText(nextDeparture.deltatime + ' minuter')
        self.mot1.setText(nextDeparture.direction)

        nextDeparture = data[self.stopList[1]][0]
        self.vagn2.setText(nextDeparture.name)
        self.time2.setText(nextDeparture.deltatime + ' minuter')
        self.mot2.setText(nextDeparture.direction)

    def createTable(self, data):
        # Create table - not used at the moment
        self.tableWidget.setRowCount(len(data['Lantmilsgatan'] )+ 1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Avgång"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Mot"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Tid"))



        for i in range(1, len(data['Lantmilsgatan']) + 1):
            nextDeparture = data['Lantmilsgatan'][i-1]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(nextDeparture.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(nextDeparture.direction))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(nextDeparture.time.strftime("%Y-%m-%d %H:%M")))

        self.tableWidget.move(0, 0)

