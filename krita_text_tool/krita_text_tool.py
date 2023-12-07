import sys
from krita import *

from .make_v_text import check


class MyExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def make_v_text(self):
        check()

    def createActions(self, window):
        action = window.createAction("myAction", "My Script", "tools/scripts")
        action.triggered.connect(self.make_v_text)
        pass


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(MyExtension(Krita.instance()))
