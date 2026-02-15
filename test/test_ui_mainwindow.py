from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.mainwindowEx import MainWindowEx

app=QApplication([])
gui=MainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()
