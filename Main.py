import sys
from GUI import TOGO_UI
from PyQt5.QtWidgets import QApplication
from Model import Model
from TOGOController import TOGOController

"""Main file, program is started from here"""
def main():
    stopList = ['Lindholmen', 'Lindholmspiren']
    app = QApplication(sys.argv)
    view = TOGO_UI(stopList)
    view.show()

    model = Model(stopList)
    controller = TOGOController(model, view) #GUI and Model are managed from controller
    # Execute the calculator's main loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
