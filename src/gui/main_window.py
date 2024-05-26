from .checking_sector import CheckingSector, SectorState
from .flashing_rectangle import FlashingRectangle
from .ui_main_window import Ui_MainWindow
from loguru import logger

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPoint, QTimer, QRect

RIGHT_WING_POINT = QPoint(27, 275)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setFixedSize(570, 700)
        self.setStyleSheet("background-image: url(./res/plane_model.png)")
        self.sector = CheckingSector(self)
        self.sector.set_state(SectorState.DISTANCE_1)
        self.sector.move(RIGHT_WING_POINT - QPoint(0, 120))
        self.sector.show()
        QTimer.singleShot(3000, lambda: self.sector.set_state(SectorState.DISTANCE_3))
        

    
