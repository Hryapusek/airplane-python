# Import the necessary module for creating the application
from PyQt5.QtWidgets import QApplication
# Import the main window class from the gui module
from gui.main_window import MainWindow


# Define the main function
def main():
    # Create an instance of the QApplication class
    app = QApplication([])
    # Create an instance of the MainWindow class
    widget = MainWindow()
    # Show the main window
    widget.show()
    # Start the application's event loop
    app.exec_()

# Check if this script is being run directly (not being imported)
if __name__ == "__main__":
    # Call the main function
    main()
