from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QRect
from .flashing_rectangle import FlashingRectangle

from states import *

SECTOR_HEIGHT = 120
HEIGHT_MARGIN = 20
WIDTH = 40
WIDTH_MARGIN = 40
SQUARE_HEIGHT = SECTOR_HEIGHT/3
SQUARE_WIDTH = WIDTH

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
                #play sound
                top_left = QPoint(0, SQUARE_HEIGHT*2)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*3)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 7, 100, "1 метр")
            elif new_state == State.DISTANCE_2:
                #play sound
                top_left = QPoint(0, SQUARE_HEIGHT)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*2)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 5, 200, "2 метра")
            elif new_state == State.DISTANCE_3:
                #play sound
                top_left = QPoint(0, 0)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 3, 300, "3 метра")
            self.__state = new_state
            self.update()
