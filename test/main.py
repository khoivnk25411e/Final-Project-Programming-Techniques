import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from Event_Check_in_Management.Ui_ex.LoginWindowEx import LoginWindowEx


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_window = LoginWindowEx()
    main_window.setupUi(QMainWindow())
    main_window.showWindow()
    
    sys.exit(app.exec())
