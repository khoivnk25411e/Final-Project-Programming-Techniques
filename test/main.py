import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.MainWindowEx import MainWindowEx

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindowEx()
    main_window.setupUi(QMainWindow())
    main_window.showWindow()
    sys.exit(app.exec())
