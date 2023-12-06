import sys

import krita as k


class MyExtension(k.Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        # Print python version
        print(sys.version)
        pass

    def createActions(self, window):
        pass


# And add the extension to Krita's list of extensions:
k.Krita.instance().addExtension(MyExtension(k.Krita.instance()))
