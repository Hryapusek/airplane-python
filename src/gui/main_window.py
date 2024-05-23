from PyQt5.QtGui import QPaintEvent
from .ui_main_window import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import QRect, QTimer


class Rectangle(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.show()
        self.shown = True
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        if self.shown:
            self.hide()
        else:
            self.show()
        self.shown = not self.shown

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))  
        qp.setBrush(br)   
        qp.drawRect(0, 0, 40, 40)
    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setFixedSize(570, 700)
        self.setStyleSheet("background-image: url(/home/hryapusek/work/repet/airplane-python/res/plane_model.png)")
        self.rectangle = Rectangle(self)
        QTimer.singleShot(2000, self.removeRectangle)

    def removeRectangle(self):
        self.rectangle.deleteLater()
