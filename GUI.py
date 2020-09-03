import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from Model import Model
from TOGOController import TOGOController


class TOGO_UI(QMainWindow):

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('DirigentgatanTOGO')
        self.generalLayout = QGridLayout()
        # Set the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()

    def _createDisplay(self):
        self.generalLayout.addWidget(QLabel('<p style="text-align:center;"><h1>DirigentgatanTOGO</h1></p>'), 0, 0, 1, 3)
        self.generalLayout.addWidget(QLabel('Lantmilsgatan'), 1, 0)

        self.generalLayout.addWidget(QLabel('Avgång'), 2, 0)
        self.generalLayout.addWidget(QLabel('Mot'), 2, 1)
        self.generalLayout.addWidget(QLabel('Tid'), 2, 2)
        self.vagn1 = QLabel('Spårvagn 1')
        self.generalLayout.addWidget(self.vagn1, 3, 0)
        self.mot1 = QLabel('Frölunda')
        self.generalLayout.addWidget(self.mot1, 3, 1)
        self.time1 = QLabel('2 minuter')
        self.generalLayout.addWidget(self.time1, 3, 2)

        self.generalLayout.addWidget(QLabel('Fyrktorget'), 4, 0)

        self.generalLayout.addWidget(QLabel('Avgång'), 5, 0)
        self.generalLayout.addWidget(QLabel('Mot'), 5, 1)
        self.generalLayout.addWidget(QLabel('Tid'), 5, 2)
        self.vagn2 = QLabel('Buss 16')
        self.generalLayout.addWidget(self.vagn2, 6, 0)
        self.mot2 = QLabel('Ekträgatan')
        self.generalLayout.addWidget(self.mot2, 6, 1)
        self.time2 = QLabel('2 minuter')
        self.generalLayout.addWidget(self.time2, 6, 2)

        self.updateButton = QPushButton('Uppdatera')
        self.generalLayout.addWidget(self.updateButton, 7, 1)

        #self.tableWidget = QTableWidget()
        #self.generalLayout.addWidget(self.tableWidget, 8, 0, 1, 3)


    def updateView(self, data):
        nextDeparture = data['Lindholmen'][0]
        self.vagn1.setText(nextDeparture.name)
        self.time1.setText(nextDeparture.time.strftime( "%Y-%m-%d %H:%M"))
        self.mot1.setText(nextDeparture.direction)

        nextDeparture = data['Lindholmspiren'][0]
        self.vagn2.setText(nextDeparture.name)
        self.time2.setText(nextDeparture.time.strftime("%Y-%m-%d %H:%M"))
        self.mot2.setText(nextDeparture.direction)

    def createTable(self, data):
        # Create table
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

def main():
    app = QApplication(sys.argv)
    view = TOGO_UI()
    view.show()

    model = Model()
    controller = TOGOController(model, view)
    # Execute the calculator's main loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
