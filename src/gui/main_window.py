from PyQt5.QtGui import QPaintEvent
from .ui_main_window import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import QRect, QTimer
    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setFixedSize(570, 700)
        self.setStyleSheet("background-image: url(./res/plane_model.png)")
