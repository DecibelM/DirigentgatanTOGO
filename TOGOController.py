from functools import partial
from PyQt5.QtCore import QTimer, QTime, Qt

class TOGOController:
    """PyCalc Controller class."""
    def __init__(self, model, view):
        """Controller initializer."""
        self._view = view
        self.model = model
        # Connect signals and slots
        self._view.updateButton.clicked.connect(partial(self.update))
        self.update()
        self.automaticUpdate()

    def update(self):
        data = self.model.update()
        self._view.updateView(data)
        print("I'm called")

    def automaticUpdate(self):
        print("Time: I'm initiated")
        # creating a timer object
        timer = QTimer()
        # adding action to timer
        timer.timeout.connect(self.update)
        # update the timer every 30 second
        timer.start(1000)