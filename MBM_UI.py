import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *
 
class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        layout  = QHBoxLayout(self)

        picture = PictureLabel("Images\\go.png", self)
        picture.pictureClicked.connect(self.anotherSlot)

        layout.addWidget(picture)
        layout.addWidget(QLabel("click on the picture"))

    def anotherSlot(self, passed):
        print ("now I'm in Main.anotherSlot")


class PictureLabel(QLabel):

    pictureClicked = Signal(str) # can be other types (list, dict, object...)

    def __init__(self, image, parent=None):
        super(PictureLabel, self).__init__(parent)        
        self.setPixmap(image)

    def mousePressEvent(self, event):
        print ("from PictureLabel.mousePressEvent")
        self.pictureClicked.emit("emit the signal")

a = QApplication([])
m = Main()
m.show()
sys.exit(a.exec_())
