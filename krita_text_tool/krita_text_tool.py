import sys
from krita import *

from .make_vertical_text import make_active_text_vertical


class TextExtension(Extension):
    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def make_v_text(self):
        make_active_text_vertical()

    def createActions(self, window):
        action = window.createAction("myAction", "Make Text Vertical", "tools/scripts")
        action.triggered.connect(self.make_v_text)

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(MyExtension(Krita.instance()))
