import sys
from GUI import TOGO_UI
from PyQt5.QtWidgets import QApplication
from Model import Model
from TOGOController import TOGOController

def main():
    stopList = ['Lindholmen', 'Lindholmspiren']
    app = QApplication(sys.argv)
    view = TOGO_UI(stopList)
    view.show()

    model = Model(stopList)
    controller = TOGOController(model, view)
    # Execute the calculator's main loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()