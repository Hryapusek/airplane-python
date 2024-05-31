from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QColor
from .flashing_rectangle import FlashingRectangle

# Import all states from the states module
from states import *

# Define constants for sector dimensions
SECTOR_HEIGHT = 120
HEIGHT_MARGIN = 20
WIDTH = 40
WIDTH_MARGIN = 80
SQUARE_HEIGHT = SECTOR_HEIGHT//3
SQUARE_WIDTH = WIDTH

# Define colors for different states
M1_COLOR = QColor("red")
M2_COLOR = QColor("orange")
M3_COLOR = QColor("yellow")

class CheckingSector(QWidget):
    def __init__(self, parent):
        # Initialize the superclass
        super().__init__(parent)
        # Set the fixed size of the widget
        self.setFixedSize(WIDTH + WIDTH_MARGIN, SECTOR_HEIGHT + HEIGHT_MARGIN)
        # Initialize the state to SAFE_DISTANCE
        self.__state = State.SAFE_DISTANCE
        # Initialize the rectangle to None
        self.__rectangle: FlashingRectangle = None

    def set_state(self, new_state: State):
        # Check if the new state is different from the current state
        if new_state != self.__state:
            # If a rectangle exists, delete it and set it to None
            if self.__rectangle is not None:
                self.__rectangle.deleteLater()
                self.__rectangle = None
            # Set the rectangle based on the new state
            if new_state == State.DISTANCE_1:
                # Calculate the top-left and bottom-right points for the rectangle
                top_left = QPoint(0, SQUARE_HEIGHT*2)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*3)
                # Create a FlashingRectangle with the specified parameters
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 7, 100, "1 метр", M1_COLOR)
            elif new_state == State.DISTANCE_2:
                top_left = QPoint(0, SQUARE_HEIGHT)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT*2)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 5, 200, "2 метра", M2_COLOR)
            elif new_state == State.DISTANCE_3:
                top_left = QPoint(0, 0)
                bottom_right = QPoint(SQUARE_WIDTH, SQUARE_HEIGHT)
                self.__rectangle = FlashingRectangle(self, QRect(top_left, bottom_right), 3, 300, "3 метра", M3_COLOR)
            # Update the state and trigger a repaint
            self.__state = new_state
            self.update()
