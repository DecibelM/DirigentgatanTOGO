from functools import partial

class TOGOController:
    """PyCalc Controller class."""
    def __init__(self, model, view):
        """Controller initializer."""
        self._view = view
        self.model = model
        # Connect signals and slots
        self._view.updateButton.clicked.connect(partial(self.update))
        self._view.updateView(model.update())

    def update(self):
        data = self.model.update()
        self._view.updateView(data)
        #self._view.createTable(data)
        #hej
