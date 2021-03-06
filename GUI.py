from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget,QMessageBox
from PyQt5.QtCore import QTime

"""GUI class which inherits from QMainWindow"""
class TOGO_UI(QMainWindow):
    """Constructor for TOGO_UI"""
    def __init__(self,stopList):
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
        self.popupMessageBox = QMessageBox()

    """Creates the initial display"""
    def _createDisplay(self):
        #Adds the image
        image = QLabel()
        pixmap = QPixmap('Travel_logga_color.png')
        image.setPixmap(pixmap.scaled(image.size()*0.5, QtCore.Qt.KeepAspectRatio))
        self.generalLayout.addWidget(image, 0, 0, 1, 3)

        #Style sheet for formatting headlines.
        styleSheet = "padding-top: 10px; padding-left:-5px; padding-right:5px; " \
                        "padding-bottom :10px; color: #785456"

        #Creating and formatting of label headlines
        label1 = QLabel('<h2>Linje</h2>')
        label2 = QLabel('<h2>Hållplats</h2>')
        label3 = QLabel('<h2>Mot</h2>')
        label4 = QLabel('<h2>Om</h2>')
        self.generalLayout.addWidget(label1, 1, 0)
        self.generalLayout.addWidget(label2, 1, 1)
        self.generalLayout.addWidget(label3, 1, 2)
        self.generalLayout.addWidget(label4, 1, 3)

        label1.setStyleSheet(styleSheet)
        label2.setStyleSheet(styleSheet)
        label3.setStyleSheet(styleSheet)
        label4.setStyleSheet(styleSheet)

        listLen=20 * len(self.stopList) # Max 20 entries per stop
        self.widgetListName = [None] * listLen
        self.widgetListStopTrack = [None] * listLen
        self.widgetListDirection = [None] * listLen
        self.widgetListDeltatime = [None] * listLen

        # creating a label object for time and adding it to the display
        self.timelabel = QLabel()
        self.generalLayout.addWidget(self.timelabel,0,3)

    """Gets current time and sets the time in GUI"""
    def getQTime(self):
        qttime = QTime.currentTime()
        label_time = '<h1>' + qttime.toString('hh:mm') + '</h1>'
        self.timelabel.setText(label_time)
        self.timelabel.setStyleSheet("padding-top : 15px;"
                             "padding-left:0px;"
                             "padding-right:30px;"
                             "padding-bottom :0px;"
                                     "font-size: 22px;"
                                     "color: #6F8089")

    """Updates the view with the latest data from the database"""
    def updateView(self, data):
        self.getQTime()
        for j in range(0,len(data)):
            nextEntry=data[j]
            if self.widgetListName[j] is None:
                self.widgetListName[j]=QLabel("<center>" + nextEntry.name + "</center>")
                self.widgetListName[j].setStyleSheet("background-color :" + nextEntry.fgColor + "; color :"
                                                     + nextEntry.bgColor)
                self.generalLayout.addWidget(self.widgetListName[j], j + 2, 0)
                self.widgetListStopTrack[j]=QLabel(nextEntry.stop +", "+nextEntry.track)
                self.generalLayout.addWidget(self.widgetListStopTrack[j], j + 2, 1)
                self.widgetListDirection[j]=QLabel(nextEntry.direction)
                self.generalLayout.addWidget(self.widgetListDirection[j], j + 2, 2)
                self.widgetListDeltatime[j]=QLabel(nextEntry.deltatime + ' min')
                self.generalLayout.addWidget(self.widgetListDeltatime[j], j + 2, 3)
            else:
                self.widgetListName[j].setText("<center>" + nextEntry.name + "</center>")
                self.widgetListName[j].setStyleSheet("background-color :" + nextEntry.fgColor + "; color :"
                                                     + nextEntry.bgColor)
                self.widgetListStopTrack[j].setText(nextEntry.stop + ", " + nextEntry.track)
                self.widgetListDirection[j].setText(nextEntry.direction)
                self.widgetListDeltatime[j].setText(nextEntry.deltatime + ' min')
        for i in range(len(data),len(self.widgetListName)):
            if self.widgetListName[i] is not None:
                self.generalLayout.removeWidget(self.widgetListName[i])
                self.widgetListName[i].deleteLater()
                self.widgetListName[i] = None
                self.generalLayout.removeWidget(self.widgetListStopTrack[i])
                self.widgetListStopTrack[i].deleteLater()
                self.widgetListStopTrack[i] = None
                self.generalLayout.removeWidget(self.widgetListDirection[i])
                self.widgetListDirection[i].deleteLater()
                self.widgetListDirection[i] = None
                self.generalLayout.removeWidget(self.widgetListDeltatime[i])
                self.widgetListDeltatime[i].deleteLater()
                self.widgetListDeltatime[i] = None

    def handleErrors(self,errorInfo):
        self.popupMessageBox.setWindowTitle("Pop-up Travel by Sigma")
        if "ValueError" in errorInfo:
            self.popupMessageBox.setText("Value Error")
            self.popupMessageBox.setIcon(QMessageBox.Warning) #Critical, Warning, Information, Question
            self.popupMessageBox.setDetailedText(str(errorInfo))
            x = self.popupMessageBox.show()  # this will show the pop up
        elif "ConnectionError" in errorInfo:
            self.popupMessageBox.setText("Connection Error")
            self.popupMessageBox.setIcon(QMessageBox.Critical)  # Critical, Warning, Information, Question
            self.popupMessageBox.setDetailedText(str(errorInfo))
            x = self.popupMessageBox.exec_()  # for stopping program in background
        else:
            self.popupMessageBox.setText("Unknown Error")
            self.popupMessageBox.setIcon(QMessageBox.Critical)  # Critical, Warning, Information, Question
            self.popupMessageBox.setDetailedText(str(errorInfo))
            x = self.popupMessageBox.exec_()  # for stopping program in background