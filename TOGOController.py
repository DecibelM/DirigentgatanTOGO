from functools import partial
from PyQt5.QtCore import QTimer

class TOGOController:
    """PyCalc Controller class."""
    def __init__(self, model, view):
        """Controller initializer."""
        self._view = view
        self.model = model
        self.data = ""
        self.update()
        self.automaticUpdate()

    def update(self):
        data = self.model.update()
        if "Error" in data:
            self._view.updateView(self.data)
            print("In controller: Error with status code " + str(data[1]))
        else:
            self.data=data
            self._view.updateView(self.data)

    def automaticUpdate(self):
        # creating a timer object
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.update)
        # update the timer every 30 second
        self.timer.start(10000)

