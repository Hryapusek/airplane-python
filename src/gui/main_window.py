from .checking_sector import *
from .flashing_rectangle import FlashingRectangle
from .ui_main_window import Ui_MainWindow
from loguru import logger
from soundplayer.sound_player import SoundPlayer

import requests

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QPoint, QTimer, QRect

RIGHT_WING_POINT = QPoint(27, 320)
RIGHT_STABILIZER_POINT = QPoint(203, 152)
LEFT_STABILIZER_POINT = QPoint(365, 152) - QPoint(WIDTH, 0)
LEFT_WING_POINT = QPoint(539, 320) - QPoint(WIDTH, 0)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 570

LEFT_WING_PORT = 32105
RIGHT_WING_PORT = LEFT_WING_PORT + 1
LEFT_STABILIZER_PORT = RIGHT_WING_PORT + 1
RIGHT_STABILIZER_PORT = LEFT_STABILIZER_PORT + 1
TIMEOUT = 3
INTERVAL = 200

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-image: url(./res/plane_model.png)")

        self.sound_player = SoundPlayer()

        self.right_wing_sector = CheckingSector(self)
        self.right_wing_sector.move(RIGHT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        self.right_stabilizer_sector = CheckingSector(self)
        self.right_stabilizer_sector.move(RIGHT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_stabilizer_sector = CheckingSector(self)
        self.left_stabilizer_sector.move(LEFT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_wing_sector = CheckingSector(self)
        self.left_wing_sector.move(LEFT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        self._ui.connect_btn.clicked.connect(lambda : self.__connect_button_clicked())

        self.labels = [self._ui.lw_con_label, self._ui.ls_con_label, self._ui.rs_con_label, self._ui.rw_con_label]
        self.ports = [LEFT_WING_PORT, LEFT_STABILIZER_PORT, RIGHT_STABILIZER_PORT, RIGHT_WING_PORT]
        self.sectors = [self.left_wing_sector, self.left_stabilizer_sector, self.right_stabilizer_sector, self.right_wing_sector]
        self.__connect_button_clicked(show_boxes=False)

    def __connect_button_clicked(self, show_boxes: bool = True):
        any_failed = False
        for label, port in zip(self.labels, self.ports):
            try:
                response = requests.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                if not response.ok:
                    raise requests.HTTPError()                
                label.setStyleSheet("color : green")
                label.setText("Соединение установлено!")
            except:
                any_failed = True
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")

        if any_failed:
            if show_boxes: self.show_connection_error_box()
        else:
            if show_boxes: QMessageBox.information(self, "Успех", "Подключение к датчикам было успешно установлено!")
            QTimer.singleShot(INTERVAL, self.__ask_detectors)
        
    def __ask_detectors(self):
        most_critical_state = State.SAFE_DISTANCE
        for sector, label, port in zip(self.sectors, self.labels, self.ports):
            try:
                response = requests.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                if not response.ok:
                    raise requests.HTTPError()
                distance = response.json()['distance']
                if distance <= 1:
                    new_state = State.DISTANCE_1
                elif distance <= 2:
                    new_state = State.DISTANCE_2
                elif distance <= 3:
                    new_state = State.DISTANCE_3
                else:
                    new_state = State.SAFE_DISTANCE
                most_critical_state = State(min(new_state.value, most_critical_state.value))
                sector.set_state(new_state)
            except:
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")
                self.sound_player.set_state(State.SAFE_DISTANCE)
                self.show_connection_error_box()
                return
        self.sound_player.set_state(most_critical_state)
        QTimer.singleShot(INTERVAL, self.__ask_detectors)

    def show_connection_error_box(self):
        QMessageBox.critical(self, "Ошибка подключения.", "Не удалось подключиться к одному из датчиков!")
