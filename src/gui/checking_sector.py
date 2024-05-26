from enum import Enum
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QRect
from .flashing_rectangle import FlashingRectangle

class SectorState(Enum):
    SAFE_DISTANCE = 0
    DISTANCE_1 = 1
    DISTANCE_2 = 2
    DISTANCE_3 = 3

SECTOR_HEIGHT = 120
WIDTH = 40
SQUARE_HEIGHT = SECTOR_HEIGHT/3
SQUARE_WIDTH = WIDTH

class CheckingSector(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(SECTOR_HEIGHT, WIDTH)
        self.__state = SectorState.SAFE_DISTANCE
        self.__rectangle: FlashingRectangle = None

    def set_state(self, new_state: SectorState):
        if new_state != self.__state:
            if self.__rectangle is not None:
                self.__rectangle.deleteLater()
                self.__rectangle = None
            if new_state == SectorState.DISTANCE_1:
                #play sound
                top_left = QPoint(0, SQUARE_HEIGHT*2)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*3)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 6, 100)
            elif new_state == SectorState.DISTANCE_2:
                #play sound
                top_left = QPoint(0, SQUARE_HEIGHT)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*2)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 4, 200)
            elif new_state == SectorState.DISTANCE_3:
                #play sound
                top_left = QPoint(0, 0)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 2, 300)
            self.__state = new_state
