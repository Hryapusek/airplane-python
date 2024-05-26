import multiprocessing
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    multiprocessing.freeze_support()
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
