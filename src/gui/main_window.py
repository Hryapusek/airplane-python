# Import necessary modules from concurrent.futures
from concurrent.futures import Future, TimeoutError as FTimeoutError

# Import requests module for making HTTP requests
import requests
# Import checking_sector module
from .checking_sector import *
# Import flashing_rectangle module
from .flashing_rectangle import FlashingRectangle
# Import ui_main_window module
from .ui_main_window import Ui_MainWindow
# Import logger from loguru
from loguru import logger
# Import SoundPlayer from soundplayer module
from soundplayer.sound_player import SoundPlayer

# Import sessions from requests_futures
from requests_futures import sessions
# Import Response from requests
from requests import Response

# Import necessary modules from PyQt5
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp
from PyQt5.QtCore import QPoint, QTimer

# Define constants for points
RIGHT_WING_POINT = QPoint(65, 355)
RIGHT_STABILIZER_POINT = QPoint(295, 130)
LEFT_STABILIZER_POINT = QPoint(507, 130) - QPoint(WIDTH, 0)
LEFT_WING_POINT = QPoint(735, 355) - QPoint(WIDTH, 0)

# Define constants for window dimensions
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 800

# Define constants for ports
LEFT_WING_PORT = 32105
RIGHT_WING_PORT = LEFT_WING_PORT + 1
LEFT_STABILIZER_PORT = RIGHT_WING_PORT + 1
RIGHT_STABILIZER_PORT = LEFT_STABILIZER_PORT + 1
TIMEOUT = 3
INTERVAL = 200

class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize superclass
        super(MainWindow, self).__init__()
        # Initialize UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        # Set fixed window size
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # Set window style
        style = """
QMainWindow
{
background-image: url(./res/plane_model.png);
background-repeat: no-repeat;
background-color: white;
}
"""
        self.setStyleSheet(style)

        # Initialize sound player
        self.sound_player = SoundPlayer()

        # Initialize sectors
        self.right_wing_sector = CheckingSector(self)
        self.right_wing_sector.move(RIGHT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        self.right_stabilizer_sector = CheckingSector(self)
        self.right_stabilizer_sector.move(RIGHT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_stabilizer_sector = CheckingSector(self)
        self.left_stabilizer_sector.move(LEFT_STABILIZER_POINT - QPoint(0, SECTOR_HEIGHT))

        self.left_wing_sector = CheckingSector(self)
        self.left_wing_sector.move(LEFT_WING_POINT - QPoint(0, SECTOR_HEIGHT))

        # Connect button click event
        self._ui.connect_btn.clicked.connect(lambda : self.__connect_button_clicked())

        # Initialize labels, ports, and sectors
        self.labels = [self._ui.lw_con_label, self._ui.ls_con_label, self._ui.rs_con_label, self._ui.rw_con_label]
        self.ports = [LEFT_WING_PORT, LEFT_STABILIZER_PORT, RIGHT_STABILIZER_PORT, RIGHT_WING_PORT]
        self.sectors = [self.left_wing_sector, self.left_stabilizer_sector, self.right_stabilizer_sector, self.right_wing_sector]
        # Call connect button click event
        self.__connect_button_clicked(show_boxes=False)

    def __connect_button_clicked(self, show_boxes: bool = True):
        # Initialize flag for connection failure
        any_failed = False
        # Create a FuturesSession with one worker
        session = sessions.FuturesSession(max_workers=1)
        # Iterate over labels and ports
        for label, port in zip(self.labels, self.ports):
            try:
                # Make a GET request to the port with a timeout
                response_future: Future[Response] = session.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                # Wait for the response with a timeout of 0.05 seconds
                while True:
                    try:
                        response = response_future.result(0.05)
                        break
                    except FTimeoutError:
                        # Process events to keep the GUI responsive
                        qApp.processEvents()
                # Process events to keep the GUI responsive
                qApp.processEvents()
                # Check if the response is OK
                if not response.ok:
                    raise requests.HTTPError()                
                # Set label style and text
                label.setStyleSheet("color : green")
                label.setText("Соединение установлено!")
            except:
                # Set flag for connection failure
                any_failed = True
                # Set label style and text
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")

        # Check if any connection failed
        if any_failed:
            # Show connection error box if show_boxes is True
            if show_boxes: self.show_connection_error_box()
        else:
            # Show success message box if show_boxes is True
            if show_boxes: QMessageBox.information(self, "Успех", "Подключение к датчикам было успешно установлено!")
            # Call ask detectors function after INTERVAL milliseconds
            QTimer.singleShot(INTERVAL, self.__ask_detectors)
    
    def __ask_detectors(self):
        # Initialize most critical state
        most_critical_state = State.SAFE_DISTANCE
        # Process events to keep the GUI responsive
        qApp.processEvents()
        # Create a FuturesSession with one worker
        session = sessions.FuturesSession(max_workers=1)
        # Process events to keep the GUI responsive
        qApp.processEvents()
        # Iterate over sectors, labels, and ports
        for sector, label, port in zip(self.sectors, self.labels, self.ports):
            try:
                # Make a GET request to the port with a timeout
                response_future: Future[Response] = session.get(f"http://localhost:{port}/distance", timeout=TIMEOUT)
                # Wait for the response with a timeout of 0.05 seconds
                while True:
                    try:
                        response = response_future.result(0.05)
                        break
                    except FTimeoutError:
                        # Process events to keep the GUI responsive
                        qApp.processEvents()
                # Process events to keep the GUI responsive
                qApp.processEvents()
                # Check if the response is OK
                if not response.ok:
                    raise requests.HTTPError()  
                # Get distance from response
                distance = response.json()['distance']
                # Determine new state based on distance
                if distance <= 1:
                    new_state = State.DISTANCE_1
                elif distance <= 2:
                    new_state = State.DISTANCE_2
                elif distance <= 3:
                    new_state = State.DISTANCE_3
                else:
                    new_state = State.SAFE_DISTANCE
                # Update most critical state
                most_critical_state = State(min(new_state.value, most_critical_state.value))
                # Set sector state
                sector.set_state(new_state)
            except Exception as e:
                # Set label style and text
                label.setStyleSheet("color : red")
                label.setText("Соединение не установлено!")
                # Set sound player state
                self.sound_player.set_state(State.SAFE_DISTANCE)
                # Show connection error box
                self.show_connection_error_box()
                return
        # Set sound player state
        self.sound_player.set_state(most_critical_state)
        # Call ask detectors function after INTERVAL milliseconds
        QTimer.singleShot(INTERVAL, self.__ask_detectors)

    def show_connection_error_box(self):
        # Show critical message box
        QMessageBox.critical(self, "Ошибка подключения.", "Не удалось подключиться к одному из датчиков!")
