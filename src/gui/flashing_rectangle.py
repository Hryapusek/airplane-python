from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QRect, QSize, Qt, QPoint


class FlashingRectangle(QWidget):
    def __init__(self, parent, rectangle: QRect, flash_count: int, interval_msec: int, text, color: QColor):
        super().__init__(parent)
        self.move(rectangle.x(), rectangle.y())
        self.resize(rectangle.size() + QSize(80, 20))
        self.__rectangle = rectangle
        self.__current_flash_count = 0
        self.__interval_msec = interval_msec
        self.__color = color
        self.flash_count = flash_count
        self.text = text
        self.show()
        QTimer.singleShot(interval_msec, self.timeout)

    def timeout(self):
        if self.isHidden():
            self.show()
            self.__current_flash_count += 1
        else:
            self.hide()
        if self.__current_flash_count < self.flash_count:
            QTimer.singleShot(self.__interval_msec, self.timeout)

    def paintEvent(self, event):
        qp = QPainter(self)
        font = qp.font()
        font.setPointSize(12)
        qp.setFont(font)
        br = QBrush(self.__color)
        qp.setBrush(br)
        pen = QPen()
        qp.setPen(pen)
        qp.drawRect(0, 0, self.__rectangle.width(), self.__rectangle.height())
        qp.drawText(QPoint(0, self.__rectangle.height() + 15), self.text)
