from ui.LoginWindow import Ui_LoginWindow


class LoginWindowEx(Ui_LoginWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.load_remember()

    def showWindow(self):
        self.MainWindow.show()