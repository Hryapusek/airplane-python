# Импортируем необходимые модули из concurrent.futures
from concurrent.futures import Future, TimeoutError as FTimeoutError

# Импортируем модуль requests для отправки HTTP-запросов
import requests
# Импортируем модуль checking_sector
from .checking_sector import *
# Импортируем модуль flashing_rectangle
from .flashing_rectangle import FlashingRectangle
# Импортируем модуль ui_main_window
from .ui_main_window import Ui_MainWindow
# Импортируем логгер из loguru
from loguru import logger
# Импортируем SoundPlayer из soundplayer
from soundplayer.sound_player import SoundPlayer

# Импортируем сессии из requests_futures
from requests_futures import sessions
# Импортируем Response из requests
from requests import Response

# Импортируем необходимые модули из PyQt5
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp
from PyQt5.QtCore import QPoint, QTimer

# Определяем константы для точек
RIGHT_WING_POINT = QPoint(65, 355)
RIGHT_STABILIZER_POINT = QPoint(295, 130)
LEFT_STABILIZER_POINT = QPoint(507, 130) - QPoint(WIDTH, 0)
LEFT_WING_POINT = QPoint(735, 355) - QPoint(WIDTH, 0)

# Определяем константы для размеров окна
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 800

# Определяем константы для портов
LEFT_WING_PORT = 32105
RIGHT_WING_PORT = LEFT_WING_PORT + 1
LEFT_STABILIZER_PORT = RIGHT_WING_PORT + 1
RIGHT_STABILIZER_PORT = LEFT_STABILIZER_PORT + 1
TIMEOUT = 0.2
INTERVAL = 200

class MainWindow(QMainWindow):
    def __init__(self):
        # Инициализируем суперкласс
        super(MainWindow, self).__init__()
        # Инициализируем UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        # Устанавливаем фиксированный размер окна
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Устанавливаем стиль окна
        style = """
QMainWindow
{
background-image: url(./res/plane_model.png);
background-repeat: no-repeat;
background-color: white;
}
"""
        self.setStyleSheet(style)

        # Инициализируем проигрыватель звука
        self.sound_player = SoundPlayer()

        # Инициализируем сектора
        self.right_wing_sector = CheckingSector(self)
        self.right_wing_sector.move(RIGHT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        self.right_stabilizer_sector = CheckingSector(self)
        self.right_stabilizer_sector.move(RIGHT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_stabilizer_sector = CheckingSector(self)
        self.left_stabilizer_sector.move(LEFT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_wing_sector = CheckingSector(self)
        self.left_wing_sector.move(LEFT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        # Подключаем событие клика кнопки
        self._ui.connect_btn.clicked.connect(lambda : self.__connect_button_clicked())

        # Инициализируем метки, порты и сектора
        self.labels = [self._ui.lw_con_label, self._ui.ls_con_label, self._ui.rs_con_label, self._ui.rw_con_label]
        self.ports = [LEFT_WING_PORT, LEFT_STABILIZER_PORT, RIGHT_STABILIZER_PORT, RIGHT_WING_PORT]
        self.sectors = [self.left_wing_sector, self.left_stabilizer_sector, self.right_stabilizer_sector, self.right_wing_sector]
        # Вызываем событие клика кнопки
        self.__connect_button_clicked(show_boxes=False)

    def __connect_button_clicked(self, show_boxes: bool = True):
        # Инициализируем флаг для ошибки подключения
        any_failed = False
        # Создаем FuturesSession с одним рабочим
        session = sessions.FuturesSession(max_workers=1)
        # Итерируемся по меткам и портам
        for label, port in zip(self.labels, self.ports):
            try:
                # Отправляем GET-запрос на порт с таймаутом
                response_future: Future[Response] = session.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                # Ждем ответа с таймаутом 0.05 секунд
                while True:
                    try:
                        response = response_future.result(0.05)
                        break
                    except FTimeoutError:
                        # Обрабатываем события, чтобы GUI оставался отзывчивым
                        qApp.processEvents()
                # Обрабатываем события, чтобы GUI оставался отзывчивым
                qApp.processEvents()
                # Проверяем, является ли ответ OK
                if not response.ok:
                    raise requests.HTTPError()                
                # Устанавливаем стиль и текст метки
                label.setStyleSheet("color : green")
                label.setText("Соединение установлено!")
            except:
                # Устанавливаем флаг для ошибки подключения
                any_failed = True
                # Устанавливаем стиль и текст метки
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")

        # Проверяем, произошла ли ошибка подключения
        if any_failed:
            # Показываем ошибку подключения, если show_boxes=True
            if show_boxes: self.show_connection_error_box()
        else:
            # Показываем сообщение об успехе, если show_boxes=True
            if show_boxes: QMessageBox.information(self, "Успех", "Подключение к датчикам было успешно установлено!")
            # Вызываем функцию ask_detectors через INTERVAL миллисекунд
            QTimer.singleShot(INTERVAL, self.__ask_detectors)
    
    def __ask_detectors(self):
        # Инициализируем наиболее критическое состояние
        most_critical_state = State.SAFE_DISTANCE
        # Обрабатываем события, чтобы GUI оставался отзывчивым
        qApp.processEvents()
        # Создаем FuturesSession с одним рабочим
        session = sessions.FuturesSession(max_workers=1)
        # Обрабатываем события, чтобы GUI оставался отзывчивым
        qApp.processEvents()
        # Итерируемся по секторам, меткам и портам
        for sector, label, port in zip(self.sectors, self.labels, self.ports):
            try:
                # Отправляем GET-запрос на порт с таймаутом
                response_future: Future[Response] = session.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                # Ждем ответа с таймаутом 0.05 секунд
                while True:
                    try:
                        response = response_future.result(0.05)
                        break
                    except FTimeoutError:
                        # Обрабатываем события, чтобы GUI оставался отзывчивым
                        qApp.processEvents()
                # Обрабатываем события, чтобы GUI оставался отзывчивым
                qApp.processEvents()
                # Проверяем, является ли ответ OK
                if not response.ok:
                    raise requests.HTTPError()  
                # Получаем расстояние из ответа
                distance = response.json()['distance']
                # Определяем новое состояние на основе расстояния
                if distance <= 1:
                    new_state = State.DISTANCE_1
                elif distance <= 2:
                    new_state = State.DISTANCE_2
                elif distance <= 3:
                    new_state = State.DISTANCE_3
                else:
                    new_state = State.SAFE_DISTANCE
                # Обновляем наиболее критическое состояние
                most_critical_state = State(min(new_state.value, most_critical_state.value))
                # Устанавливаем состояние сектора
                sector.set_state(new_state)
            except Exception as e:
                # Устанавливаем стиль и текст метки
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")
                # Устанавливаем состояние проигрывателя звука
                self.sound_player.set_state(State.SAFE_DISTANCE)
                # Показываем ошибку подключения
                self.show_connection_error_box()
                return

        # Устанавливаем состояние проигрывателя звука
        self.sound_player.set_state(most_critical_state)
        # Вызываем функцию ask_detectors через INTERVAL миллисекунд
        QTimer.singleShot(INTERVAL, self.__ask_detectors)

    def show_connection_error_box(self):
        # Показываем критическое сообщение
        QMessageBox.critical(self, "Ошибка подключения.", "Не удалось подключиться к одному из датчиков!")
