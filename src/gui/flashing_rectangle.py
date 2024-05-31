# Import necessary modules from PyQt5
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QRect, QSize, QPoint

# Define a class FlashingRectangle that inherits from QWidget
class FlashingRectangle(QWidget):
    def __init__(self, parent, rectangle: QRect, flash_count: int, interval_msec: int, text, color: QColor):
        # Call the constructor of the superclass
        super().__init__(parent)
        
        # Move the rectangle to the specified position
        self.move(rectangle.x(), rectangle.y())
        
        # Resize the rectangle by adding a fixed size
        self.resize(rectangle.size() + QSize(120, 20))
        
        # Store the rectangle, flash count, interval, color, and text as instance variables
        self.__rectangle = rectangle
        self.__current_flash_count = 0
        self.__interval_msec = interval_msec
        self.__color = color
        self.flash_count = flash_count
        self.text = text
        
        # Show the widget
        self.show()
        
        # Schedule a timeout event after the specified interval
        QTimer.singleShot(interval_msec, self.timeout)

    # Define a method to handle the timeout event
    def timeout(self):
        # If the widget is hidden, show it and increment the flash count
        if self.isHidden():
            self.show()
            self.__current_flash_count += 1
        # If the widget is visible, hide it
        else:
            self.hide()
        
        # If the flash count is less than the specified count, schedule another timeout event
        if self.__current_flash_count < self.flash_count:
            QTimer.singleShot(self.__interval_msec, self.timeout)

    # Define a method to handle the paint event
    def paintEvent(self, event):
        # Create a QPainter object
        qp = QPainter(self)
        
        # Set the font and font size
        font = qp.font()
        font.setPointSize(12)
        qp.setFont(font)
        
        # Create a QBrush object with the specified color
        br = QBrush(self.__color)
        qp.setBrush(br)
        
        # Create a QPen object
        pen = QPen()
        qp.setPen(pen)
        
        # Draw a rectangle with the specified dimensions
        qp.drawRect(0, 0, self.__rectangle.width(), self.__rectangle.height())
        
        # Draw the text at the specified position
        qp.drawText(QPoint(0, self.__rectangle.height() + 15), self.text)
