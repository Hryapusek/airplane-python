import unittest

from PyQt5.QtWidgets import QApplication
from ..main_window import MainWindow


class TestMainWindow(unittest.TestCase):

    def test_default(self):
        app = QApplication([])
        widget = MainWindow()
        widget.show()
        app.exec_()
