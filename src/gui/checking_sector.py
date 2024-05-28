from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QColor
from .flashing_rectangle import FlashingRectangle

from states import *

SECTOR_HEIGHT = 120
HEIGHT_MARGIN = 20
WIDTH = 40
WIDTH_MARGIN = 80
SQUARE_HEIGHT = SECTOR_HEIGHT//3
SQUARE_WIDTH = WIDTH

M1_COLOR = QColor("red")
M2_COLOR = QColor("orange")
M3_COLOR = QColor("yellow")

class CheckingSector(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(WIDTH + WIDTH_MARGIN, SECTOR_HEIGHT + HEIGHT_MARGIN)
        self.__state = State.SAFE_DISTANCE
        self.__rectangle: FlashingRectangle = None

    def set_state(self, new_state: State):
        if new_state != self.__state:
            if self.__rectangle is not None:
                self.__rectangle.deleteLater()
                self.__rectangle = None
            if new_state == State.DISTANCE_1:
                top_left = QPoint(0, SQUARE_HEIGHT*2)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*3)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 7, 100, "1 метр", M1_COLOR)
            elif new_state == State.DISTANCE_2:
                top_left = QPoint(0, SQUARE_HEIGHT)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*2)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 5, 200, "2 метра", M2_COLOR)
            elif new_state == State.DISTANCE_3:
                top_left = QPoint(0, 0)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 3, 300, "3 метра", M3_COLOR)
            self.__state = new_state
            self.update()
