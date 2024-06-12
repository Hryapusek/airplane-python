# Импортируем необходимый модуль для создания приложения
from PyQt5.QtWidgets import QApplication
# Импортируем класс главного окна из модуля gui
from gui.main_window import MainWindow


# Определяем главную функцию
def main():
    # Создаем экземпляр класса QApplication
    app = QApplication([])
    # Создаем экземпляр класса MainWindow
    widget = MainWindow()
    # Показываем главное окно
    widget.show()
    # Запускаем цикл событий приложения
    app.exec_()

# Проверяем, запускается ли этот скрипт напрямую (не импортируется)
if __name__ == "__main__":
    # Вызываем главную функцию
    main()
