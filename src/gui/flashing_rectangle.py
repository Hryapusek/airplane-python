from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QRect, QSize, Qt


class FlashingRectangle(QWidget):
    def __init__(self, parent, rectangle: QRect, flash_count: int, interval_msec: int):
        super().__init__(parent)
        self.move(rectangle.x(), rectangle.y())
        self.resize(rectangle.size() + QSize(10, 10))
        self.__rectangle = rectangle
        self.__current_flash_count = 0
        self.__interval_msec = interval_msec
        self.flash_count = flash_count
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
        color = QColor()
        color.setRgb(255, 0, 0)
        br = QBrush(color)
        qp.setBrush(br)
        pen = QPen(Qt.PenStyle.NoPen)
        qp.setPen(pen)
        qp.drawRect(0, 0, self.__rectangle.width(), self.__rectangle.height())
