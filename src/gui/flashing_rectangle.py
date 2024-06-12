# Импортируем необходимые модули из PyQt5
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QRect, QSize, QPoint

# Определяем класс FlashingRectangle, который наследует от QWidget
class FlashingRectangle(QWidget):
    def __init__(self, parent, rectangle: QRect, flash_count: int, interval_msec: int, text, color: QColor):
        # Вызываем конструктор суперкласса
        super().__init__(parent)
        
        # Перемещаем прямоугольник в указанную позицию
        self.move(rectangle.x(), rectangle.y())
        
        # Изменяем размер прямоугольника, добавляя фиксированный размер
        self.resize(rectangle.size() + QSize(120, 20))
        
        # Сохраняем прямоугольник, количество вспышек, интервал, цвет и текст как переменные экземпляра
        self.__rectangle = rectangle
        self.__current_flash_count = 0
        self.__interval_msec = interval_msec
        self.__color = color
        self.flash_count = flash_count
        self.text = text
        
        # Показываем виджет
        self.show()
        
        # Планируем событие таймаута после указанного интервала
        QTimer.singleShot(interval_msec, self.timeout)

    # Определяем метод для обработки события таймаута
    def timeout(self):
        # Если виджет скрыт, показываем его и увеличиваем количество вспышек
        if self.isHidden():
            self.show()
            self.__current_flash_count += 1
        # Если виджет видим, скрываем его
        else:
            self.hide()
        
        # Если количество вспышек меньше указанного количества, планируем еще одно событие таймаута
        if self.__current_flash_count < self.flash_count:
            QTimer.singleShot(self.__interval_msec, self.timeout)

    # Определяем метод для обработки события рисования
    def paintEvent(self, event):
        # Создаем объект QPainter
        qp = QPainter(self)
        
        # Устанавливаем шрифт и размер шрифта
        font = qp.font()
        font.setPointSize(12)
        qp.setFont(font)
        
        # Создаем объект QBrush с указанным цветом
        br = QBrush(self.__color)
        qp.setBrush(br)
        
        # Создаем объект QPen
        pen = QPen()
        qp.setPen(pen)
        
        # Рисуем прямоугольник с указанными размерами
        qp.drawRect(0, 0, self.__rectangle.width(), self.__rectangle.height())
        
        # Рисуем текст в указанной позиции
        qp.drawText(QPoint(0, self.__rectangle.height() + 15), self.text)
