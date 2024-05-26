from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
