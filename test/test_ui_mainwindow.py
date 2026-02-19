from PyQt6.QtWidgets import QApplication, QMainWindow

from UI_Ex.mainwindowEx import MainWindowEx

app=QApplication([])
gui=MainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()
